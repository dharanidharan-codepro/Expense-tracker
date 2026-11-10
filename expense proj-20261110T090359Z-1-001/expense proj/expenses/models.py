"""
Expense model — stores individual expense records linked to a User.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Expense(models.Model):
    """
    Represents a single expense entry for a user.
    Each expense belongs to exactly one user.
    """

    # Category choices for predefined list
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Travel', 'Travel'),
        ('Shopping', 'Shopping'),
        ('Education', 'Education'),
        ('Entertainment', 'Entertainment'),
        ('Bills', 'Bills'),
        ('Health', 'Health'),
        ('Other', 'Other'),
    ]

    # Link to the authenticated user — cascades on delete
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')

    # Short description of what the expense was for
    description = models.CharField(max_length=255)

    # Amount in currency (supports up to 10 digits, 2 decimal places)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    # Auto-predicted or manually set category
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')

    # The date the expense occurred
    date = models.DateField()

    # Optional additional notes
    notes = models.TextField(blank=True, null=True)

    # Auto timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']  # Newest first

    def __str__(self):
        return f"{self.user.username} — {self.description} — ₹{self.amount}"
