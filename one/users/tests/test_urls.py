"""
User Test URLs
"""
import pytest
from django.urls import resolve, reverse

from one.users.models import User

pytestmark = pytest.mark.django_db


def test_detail(user: User):
    """test_detail"""
    assert (
        reverse("users:detail", kwargs={"username": user.username})
        == f"/users/{user.username}/"
    )
    assert resolve(f"/users/{user.username}/").view_name == "users:detail"


def test_update():
    """test_update"""
    assert reverse("users:update") == "/users/~update/"
    assert resolve("/users/~update/").view_name == "users:update"


def test_redirect():
    """test_redirect"""
    assert reverse("users:redirect") == "/users/~redirect/"
    assert resolve("/users/~redirect/").view_name == "users:redirect"
