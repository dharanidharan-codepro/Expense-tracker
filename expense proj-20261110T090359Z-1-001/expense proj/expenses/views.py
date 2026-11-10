"""
Views for the Smart Expense Tracker.
All views are protected with @login_required.
User data is always filtered by request.user — never exposed to other users.
"""

import json
from datetime import date, timedelta
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse

from .models import Expense
from .forms import SignupForm, ExpenseForm
from .category_predictor import predict_category
from .reports import generate_csv_report, generate_pdf_report


# ─────────────────────────────────────────────
# AUTHENTICATION VIEWS
# ─────────────────────────────────────────────

def signup_view(request):
    """
    Handles user registration.
    On GET: shows the signup form.
    On POST: validates and creates the new user, then logs them in.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been created successfully.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = SignupForm()

    return render(request, 'registration/signup.html', {'form': form})


# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────

@login_required
def dashboard(request):
    """
    Main dashboard showing:
    - Summary cards (total, today, this week, this month)
    - Recent expenses
    - Category-wise spending data for Chart.js
    - Expense trend data for Chart.js
    """
    today = date.today()
    week_start = today - timedelta(days=today.weekday())  # Monday
    month_start = today.replace(day=1)

    # All expenses for this user
    all_expenses = Expense.objects.filter(user=request.user)

    # ── Summary Cards ──
    total_all = all_expenses.aggregate(total=Sum('amount'))['total'] or Decimal('0')
    total_today = all_expenses.filter(date=today).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    total_week = all_expenses.filter(date__gte=week_start).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    total_month = all_expenses.filter(date__gte=month_start).aggregate(total=Sum('amount'))['total'] or Decimal('0')

    # ── Recent Expenses (last 5) ──
    recent_expenses = all_expenses[:5]

    # ── Category-wise data for Pie/Doughnut Chart ──
    category_data = (
        all_expenses
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )
    chart_labels = [item['category'] for item in category_data]
    chart_values = [float(item['total']) for item in category_data]

    # ── Expense Trend — last 30 days ──
    thirty_days_ago = today - timedelta(days=29)
    trend_data = (
        all_expenses
        .filter(date__gte=thirty_days_ago)
        .values('date')
        .annotate(total=Sum('amount'))
        .order_by('date')
    )
    trend_labels = [item['date'].strftime('%d %b') for item in trend_data]
    trend_values = [float(item['total']) for item in trend_data]

    context = {
        'total_all': total_all,
        'total_today': total_today,
        'total_week': total_week,
        'total_month': total_month,
        'recent_expenses': recent_expenses,
        'chart_labels': json.dumps(chart_labels),
        'chart_values': json.dumps(chart_values),
        'trend_labels': json.dumps(trend_labels),
        'trend_values': json.dumps(trend_values),
        'expense_count': all_expenses.count(),
    }
    return render(request, 'expenses/dashboard.html', context)


# ─────────────────────────────────────────────
# EXPENSE CRUD VIEWS
# ─────────────────────────────────────────────

@login_required
def expense_list(request):
    """
    Shows all expenses for the logged-in user.
    Supports filtering by: today / this_week / this_month / all (default).
    """
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)

    # Get filter from query parameter
    filter_param = request.GET.get('filter', 'all')

    # Always filter by the current user — never show other users' data
    expenses = Expense.objects.filter(user=request.user)

    if filter_param == 'today':
        expenses = expenses.filter(date=today)
    elif filter_param == 'this_week':
        expenses = expenses.filter(date__gte=week_start)
    elif filter_param == 'this_month':
        expenses = expenses.filter(date__gte=month_start)
    # 'all' — no additional filter needed

    # Calculate total for the filtered set
    total_amount = expenses.aggregate(total=Sum('amount'))['total'] or Decimal('0')

    context = {
        'expenses': expenses,
        'filter_param': filter_param,
        'total_amount': total_amount,
        'expense_count': expenses.count(),
    }
    return render(request, 'expenses/expense_list.html', context)


@login_required
def add_expense(request):
    """
    Handles adding a new expense.
    On GET: shows empty form.
    On POST: validates, auto-predicts category if not set, saves expense.
    """
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # Always assign to logged-in user

            # Auto-predict category from description if user didn't change it
            if not expense.category or expense.category == 'Other':
                expense.category = predict_category(expense.description)

            expense.save()
            messages.success(request, f'Expense "{expense.description}" added successfully!')
            return redirect('expense_list')
        else:
            messages.error(request, 'Please fix the errors below and try again.')
    else:
        # Pre-fill today's date
        form = ExpenseForm(initial={'date': date.today()})

    return render(request, 'expenses/expense_form.html', {'form': form, 'action': 'Add'})


@login_required
def edit_expense(request, pk):
    """
    Handles editing an existing expense.
    SECURITY: Uses get_object_or_404 with user=request.user to prevent
    users from editing another user's expenses by changing the URL ID.
    """
    # This will return 404 if the expense doesn't belong to the current user
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            updated_expense = form.save(commit=False)

            # Re-predict category if description changed
            updated_expense.category = predict_category(updated_expense.description)

            updated_expense.save()
            messages.success(request, 'Expense updated successfully.')
            return redirect('expense_list')
        else:
            messages.error(request, 'Please fix the errors and try again.')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'expenses/expense_form.html', {
        'form': form,
        'expense': expense,
        'action': 'Edit'
    })


@login_required
def delete_expense(request, pk):
    """
    Handles deleting an expense with a confirmation page.
    SECURITY: Only the owner can delete their own expense.
    DELETE only happens on POST — GET shows the confirmation page.
    """
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == 'POST':
        expense_description = expense.description
        expense.delete()
        messages.success(request, f'Expense "{expense_description}" deleted successfully.')
        return redirect('expense_list')

    return render(request, 'expenses/expense_confirm_delete.html', {'expense': expense})


# ─────────────────────────────────────────────
# AJAX — CATEGORY PREDICTION
# ─────────────────────────────────────────────

@login_required
def predict_category_ajax(request):
    """
    AJAX endpoint to predict category based on description input.
    Called by JavaScript as the user types in the description field.
    """
    description = request.GET.get('description', '')
    category = predict_category(description)
    return JsonResponse({'category': category})


# ─────────────────────────────────────────────
# REPORT VIEWS
# ─────────────────────────────────────────────

@login_required
def report_page(request):
    """
    Shows the report page with a summary and download options.
    """
    expenses = Expense.objects.filter(user=request.user)
    total = expenses.aggregate(total=Sum('amount'))['total'] or Decimal('0')

    context = {
        'expenses': expenses[:10],  # Show preview of 10 records
        'total': total,
        'expense_count': expenses.count(),
    }
    return render(request, 'expenses/report.html', context)


@login_required
def download_csv(request):
    """
    Generates and returns a CSV file with all the user's expenses.
    """
    expenses = Expense.objects.filter(user=request.user)
    return generate_csv_report(expenses, request.user.username)


@login_required
def download_pdf(request):
    """
    Generates and returns a PDF report with all the user's expenses.
    """
    expenses = Expense.objects.filter(user=request.user)
    return generate_pdf_report(expenses, request.user.username)
