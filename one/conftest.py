from importlib import import_module

import pytest
from django.conf import settings as conf_settings
from django.contrib.sites.models import Site
from django.http import HttpRequest

from one.contrib.sites.tests.factories import SiteFactory
from one.users.models import User
from one.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def site() -> Site:
    return SiteFactory()


@pytest.fixture()
def admin_client(
    db: None,
    admin_user,
):
    """A Django test client logged in as an admin user."""
    from django.test.client import Client

    class CustomClient(Client):
        def _login(self, user, backend=None):
            from django.contrib.auth import login

            # Create a fake request to store login details.
            request = HttpRequest()
            request.META["HTTP_X_FORWARDED_FOR"] = conf_settings.IP_PLACEHOLDER
            request.META["HTTP_USER_AGENT"] = "Macos"
            engine = import_module(conf_settings.SESSION_ENGINE)

            request.session = self.session if self.session else engine.SessionStore()

            login(request, user, backend)
            # Save the session values.
            request.session.save()
            # Set the cookie to represent the session.
            session_cookie = conf_settings.SESSION_COOKIE_NAME
            self.cookies[session_cookie] = request.session.session_key
            cookie_data = {
                "max-age": None,
                "path": "/",
                "domain": conf_settings.SESSION_COOKIE_DOMAIN,
                "secure": conf_settings.SESSION_COOKIE_SECURE or None,
                "expires": None,
            }
            self.cookies[session_cookie].update(cookie_data)

    client = CustomClient()
    client.force_login(admin_user)
    return client
