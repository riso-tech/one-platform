import pytest

from one.emails.models import AllauthTemplate

pytestmark = pytest.mark.django_db


def test_allauth_template_language_verbose(allauth: AllauthTemplate):
    """language_verbose"""
    assert allauth.language_verbose == "Vietnamese"


def test_allauth_template_update_form(allauth: AllauthTemplate):
    """language_verbose"""
    update_form = allauth.update_form
    assert "content" in update_form.fields
