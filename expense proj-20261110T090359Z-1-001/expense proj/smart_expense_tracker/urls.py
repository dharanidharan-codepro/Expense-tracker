"""
URL configuration for Smart Expense Tracker project.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Django built-in authentication (login, logout)
    path('accounts/', include('django.contrib.auth.urls')),

    # Expenses app URLs
    path('', include('expenses.urls')),

    # Redirect root to dashboard
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
]
