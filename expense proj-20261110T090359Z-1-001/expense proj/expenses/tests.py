"""
Basic tests for the Smart Expense Tracker.
Tests cover: authentication, expense CRUD, data isolation, category prediction, CSV/PDF export.
"""

from datetime import date
from decimal import Decimal

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Expense
from .category_predictor import predict_category


class CategoryPredictorTests(TestCase):
    """Tests for the keyword-based category predictor."""

    def test_food_prediction(self):
        self.assertEqual(predict_category('pizza with friends'), 'Food')

    def test_travel_prediction(self):
        self.assertEqual(predict_category('Uber ride to college'), 'Travel')

    def test_education_prediction(self):
        self.assertEqual(predict_category('Bought Python book'), 'Education')

    def test_entertainment_prediction(self):
        self.assertEqual(predict_category('Netflix subscription'), 'Entertainment')

    def test_bills_prediction(self):
        self.assertEqual(predict_category('electricity bill'), 'Bills')

    def test_health_prediction(self):
        self.assertEqual(predict_category('medicine from pharmacy'), 'Health')

    def test_shopping_prediction(self):
        self.assertEqual(predict_category('ordered from amazon'), 'Shopping')

    def test_other_prediction(self):
        self.assertEqual(predict_category('random unknown thing'), 'Other')

    def test_empty_description(self):
        self.assertEqual(predict_category(''), 'Other')

    def test_case_insensitive(self):
        self.assertEqual(predict_category('PIZZA'), 'Food')


class AuthenticationTests(TestCase):
    """Tests for signup, login, and logout."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )

    def test_signup_page_loads(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_successful_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertRedirects(response, '/dashboard/')

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, '/accounts/login/?next=/dashboard/')

    def test_expense_list_requires_login(self):
        response = self.client.get(reverse('expense_list'))
        self.assertRedirects(response, '/accounts/login/?next=/expenses/')


class ExpenseCRUDTests(TestCase):
    """Tests for creating, reading, updating, and deleting expenses."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='cruduser', password='pass123')
        self.client.login(username='cruduser', password='pass123')

        self.expense = Expense.objects.create(
            user=self.user,
            description='Test coffee',
            amount=Decimal('150.00'),
            category='Food',
            date=date.today()
        )

    def test_expense_list_loads(self):
        response = self.client.get(reverse('expense_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test coffee')

    def test_add_expense(self):
        response = self.client.post(reverse('add_expense'), {
            'description': 'Uber to station',
            'amount': '200.00',
            'date': date.today(),
            'category': 'Travel',
            'notes': ''
        })
        self.assertRedirects(response, reverse('expense_list'))
        self.assertTrue(Expense.objects.filter(description='Uber to station').exists())

    def test_edit_expense(self):
        response = self.client.post(
            reverse('edit_expense', kwargs={'pk': self.expense.pk}),
            {
                'description': 'Updated coffee description',
                'amount': '200.00',
                'date': date.today(),
                'category': 'Food',
                'notes': ''
            }
        )
        self.assertRedirects(response, reverse('expense_list'))
        self.expense.refresh_from_db()
        self.assertEqual(self.expense.description, 'Updated coffee description')

    def test_delete_expense(self):
        response = self.client.post(
            reverse('delete_expense', kwargs={'pk': self.expense.pk})
        )
        self.assertRedirects(response, reverse('expense_list'))
        self.assertFalse(Expense.objects.filter(pk=self.expense.pk).exists())

    def test_dashboard_loads(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)


class DataIsolationTests(TestCase):
    """
    Critical security tests — ensures users cannot access each other's expenses.
    """

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')

        # Create expense belonging to user1
        self.user1_expense = Expense.objects.create(
            user=self.user1,
            description='User1 private expense',
            amount=Decimal('500.00'),
            category='Other',
            date=date.today()
        )

    def test_user2_cannot_edit_user1_expense(self):
        # Login as user2
        self.client.login(username='user2', password='pass123')
        response = self.client.post(
            reverse('edit_expense', kwargs={'pk': self.user1_expense.pk}),
            {
                'description': 'Hacked!',
                'amount': '1.00',
                'date': date.today(),
                'category': 'Other',
                'notes': ''
            }
        )
        # Should return 404, not update the expense
        self.assertEqual(response.status_code, 404)
        self.user1_expense.refresh_from_db()
        self.assertEqual(self.user1_expense.description, 'User1 private expense')

    def test_user2_cannot_delete_user1_expense(self):
        self.client.login(username='user2', password='pass123')
        response = self.client.post(
            reverse('delete_expense', kwargs={'pk': self.user1_expense.pk})
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Expense.objects.filter(pk=self.user1_expense.pk).exists())

    def test_expense_list_only_shows_own_expenses(self):
        # user2 should not see user1's expenses
        self.client.login(username='user2', password='pass123')
        response = self.client.get(reverse('expense_list'))
        self.assertNotContains(response, 'User1 private expense')


class ReportTests(TestCase):
    """Tests for CSV and PDF export."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='reportuser', password='pass123')
        self.client.login(username='reportuser', password='pass123')
        Expense.objects.create(
            user=self.user,
            description='Test expense for report',
            amount=Decimal('300.00'),
            category='Food',
            date=date.today()
        )

    def test_csv_download(self):
        response = self.client.get(reverse('download_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn(b'Test expense for report', response.content)

    def test_pdf_download(self):
        response = self.client.get(reverse('download_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(response.content.startswith(b'%PDF'))
