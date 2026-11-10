"""
Admin configuration for the Expense model.
Allows site administrators to view and manage all expenses.
"""

from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for Expense model.
    Provides useful filters and display columns.
    """
    list_display = ['user', 'description', 'amount', 'category', 'date', 'created_at']
    list_filter = ['category', 'date', 'user']
    search_fields = ['description', 'user__username', 'notes']
    ordering = ['-date', '-created_at']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = [
        ('Expense Details', {
            'fields': ['user', 'description', 'amount', 'category', 'date', 'notes']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]
