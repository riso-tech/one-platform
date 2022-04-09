"""
Allauth to template context
"""
from django.conf import settings


def allauth_settings(request):
    """Expose some settings from django-allauth in templates."""
    return {
        "request": request,
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
    }
