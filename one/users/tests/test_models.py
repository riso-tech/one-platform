import datetime

import pytest
from django.conf import settings
from django.core.cache import cache

from one.users.models import User

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"


def test_user_as_avatar(user: User):
    """test_user_as_avatar"""
    assert "/static/metronic/media/svg/" in user.as_avatar


def test_user_as_name(user: User):
    """test_user_as_name"""
    assert user.as_name is not None


def test_user_as_title(user: User):
    """test_user_as_title"""
    assert user.as_title is not None


def test_user_as_choice(user: User):
    """test_user_as_choice"""
    assert user.as_choice is not None


def test_user_as_cell(user: User):
    """test_user_as_cell"""
    assert user.as_cell is not None


def test_user_as_dict(user: User):
    """test_user_as_dict"""
    assert user.as_dict is not None


def test_update_user(user: User):
    """test_update_user"""
    user.name = "Test"
    user.save()
    assert user.time_modified is not None


def test_user_last_seen(user: User):
    """test_user_last_seen"""
    assert not user.last_seen


def test_user_is_online(user: User):
    """test_user_online"""
    assert not user.is_online

    now = datetime.datetime.now()
    cache.set(
        f"seen_{user.username}",
        now,
        settings.USER_LASTSEEN_TIMEOUT,
    )
    assert user.is_online

    cache.set(
        f"seen_{user.username}",
        now - datetime.timedelta(seconds=500),
        settings.USER_LASTSEEN_TIMEOUT,
    )
    assert not user.is_online


def test_user_is_online_dot(user: User):
    """test_user_is_online_dot"""
    online = (
        '<div class="position-absolute translate-middle bottom-0 start-100 mb-6 bg-success'
        + ' rounded-circle border border-4 border-white h-20px w-20px"></div>'
    )

    offline = (
        '<div class="position-absolute translate-middle bottom-0 start-100 mb-6 bg-danger'
        + ' rounded-circle border border-4 border-white h-20px w-20px"></div>'
    )

    assert user.is_online_dot == offline

    now = datetime.datetime.now()
    cache.set(
        f"seen_{user.username}",
        now,
        settings.USER_LASTSEEN_TIMEOUT,
    )

    assert user.is_online_dot == online


def test_set_theme(user: User):
    """test_set_theme"""
    user.set_theme("dark")
    assert user.theme == settings.DARK_THEME


def test_set_language(user: User):
    """test_set_language"""
    user.set_language("en")
    assert user.language == settings.ENGLISH
