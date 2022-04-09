import pytest
from django.http import HttpRequest
from django.test import RequestFactory

from one.users.middleware import ActiveUserMiddleware

pytestmark = pytest.mark.django_db


class TestUserMiddleware:
    """
    Test Users Middleware functions
    """

    @staticmethod
    def dummy_get_response(request: HttpRequest):
        return None

    def test_active_user_middleware(self, rf: RequestFactory):
        """
        Test request without user
        :param rf:
        :return:
        """
        request = rf.get("/fake-url/")
        assert (
            ActiveUserMiddleware(self.dummy_get_response).process_request(request)
            is None
        )
