import pytest
from django.contrib.auth.models import Group
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpRequest
from django.test import RequestFactory

from one.contrib.auth.contexts.views import GroupCreateView, GroupListView
from one.users.models import User

pytestmark = pytest.mark.django_db


class TestGroupListView:
    def dummy_get_response(self, request: HttpRequest):
        return None

    def test_get_context_data(self, user: User, rf: RequestFactory):
        view = GroupListView()

        request = rf.get("/fake-url/")
        request.user = user

        view.request = request
        view.object_list = Group.objects.all()
        assert "breadcrumb" in view.get_context_data()


class TestGroupCreateView:
    def dummy_get_response(self, request: HttpRequest):
        return None

    def test_get_success_url(self, user: User, rf: RequestFactory):
        view = GroupCreateView()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_success_url() == "/~group/"

    def test_form_valid(self, user: User, rf: RequestFactory):
        view = GroupCreateView()
        request = rf.post(
            "/fake-url/",
            data={"name": "name", "avatar": "mobile_logo"},
        )
        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)

        request.user = user

        view.request = request
        response = view.post(request)
        assert response.status_code == 302

    def test_form_invalid(self, user: User, rf: RequestFactory):
        view = GroupCreateView()
        avatar = SimpleUploadedFile(
            "file.mp4", b"file_content", content_type="video/mp4"
        )
        request = rf.post("/fake-url/", data={"name": "name", "avatar": avatar})

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)

        request.user = user

        view.request = request
        response = view.post(request)
        assert response.status_code == 302
