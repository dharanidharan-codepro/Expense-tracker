"""
URL patterns for the expenses app.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('accounts/signup/', views.signup_view, name='signup'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Expense CRUD
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/add/', views.add_expense, name='add_expense'),
    path('expenses/<int:pk>/edit/', views.edit_expense, name='edit_expense'),
    path('expenses/<int:pk>/delete/', views.delete_expense, name='delete_expense'),

    # AJAX endpoint for category prediction
    path('api/predict-category/', views.predict_category_ajax, name='predict_category'),

    # Reports
    path('reports/', views.report_page, name='report_page'),
    path('reports/download/csv/', views.download_csv, name='download_csv'),
    path('reports/download/pdf/', views.download_pdf, name='download_pdf'),
]
