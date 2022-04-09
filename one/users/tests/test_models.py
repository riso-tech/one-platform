"""
User Test Model
"""
import pytest

from one.users.models import User

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user: User):
    """test_user_get_absolute_url"""
    assert user.get_absolute_url() == f"/users/{user.username}/"
