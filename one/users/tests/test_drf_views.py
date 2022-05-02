import pytest
from django.test import RequestFactory

from one.users.api.views import UserViewSet
from one.users.models import User

pytestmark = pytest.mark.django_db


class TestUserViewSet:
    def test_get_queryset(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user in view.get_queryset()

    def test_me(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        response = view.me(request)

        assert response.data == {
            "username": user.username,
            "name": user.name,
            "url": f"http://testserver/api/users/{user.username}/",
        }

    def test_set_theme(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/?theme=dark")
        request.user = user

        view.request = request

        response = view.set_theme(request)

        assert response.data == {
            "username": user.username,
            "name": user.name,
            "url": f"http://testserver/api/users/{user.username}/",
        }

    def test_set_language(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/?language=en")
        request.user = user

        view.request = request

        response = view.set_language(request)

        assert response.data == {
            "username": user.username,
            "name": user.name,
            "url": f"http://testserver/api/users/{user.username}/",
        }
