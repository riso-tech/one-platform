import pytest
from django.test import RequestFactory
from django.urls import reverse

from one.contrib.auth.contexts.api.views import GroupViewSet
from one.contrib.auth.contexts.models import Group
from one.users.models import User

pytestmark = pytest.mark.django_db


class TestGroupViewSet:
    def test_get_model(self, user: User, rf: RequestFactory):
        view = GroupViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_model() == Group

    def test_delete(self, admin_client):
        response = admin_client.delete(reverse("api:group-delete"), json=["1", "2"])

        assert response.status_code == 204
