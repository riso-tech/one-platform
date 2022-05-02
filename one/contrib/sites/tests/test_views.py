import pytest
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sites.models import Site
from django.http import HttpRequest
from django.test import RequestFactory

from one.contrib.sites.settings.views import SiteDetailView
from one.users.models import User

pytestmark = pytest.mark.django_db


class TestSiteDetailView:
    def dummy_get_response(self, request: HttpRequest):
        return None

    def test_get_success_url(self, user: User, rf: RequestFactory):
        view = SiteDetailView()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_success_url() == "/~setting/"

    def test_get_object(self, user: User, rf: RequestFactory):
        view = SiteDetailView()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_object() == Site.objects.first()

    def test_get_context_data(self, user: User, site: Site, rf: RequestFactory):
        view = SiteDetailView()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request
        view.object = site

        assert "breadcrumb" in view.get_context_data()

    def test_form_valid(self, user: User, rf: RequestFactory):
        view = SiteDetailView()
        request = rf.post(
            "/fake-url/",
            data={
                "name": "name",
                "domain": "domain",
                "favicon": "favicon",
                "logo": "logo",
                "mobile_logo": "mobile_logo",
                "site": Site.objects.first().id,
            },
        )
        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)

        request.user = user

        view.request = request
        response = view.post(request)
        assert response.status_code == 302

    def test_form_invalid(self, user: User, rf: RequestFactory):
        view = SiteDetailView()
        request = rf.post("/fake-url/")

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)

        request.user = user

        view.request = request
        response = view.post(request)
        assert response.status_code == 200
