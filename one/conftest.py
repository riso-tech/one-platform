"""
Unittest Configurations
"""
import pytest

from one.users.models import User
from one.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    """Override media_root for test"""
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    """Fixture for User model"""
    return UserFactory()
