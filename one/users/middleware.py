import datetime

from django.conf import settings
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin


class ActiveUserMiddleware(MiddlewareMixin):
    """User Middleware"""

    @staticmethod
    def process_request(request):
        """
        1. Set cache for last seen user
        :param request:
        :return:
        """
        try:
            current_user = request.user
            if current_user.is_authenticated:
                now = datetime.datetime.now()
                cache.set(
                    f"seen_{current_user.username}",
                    now,
                    settings.USER_LASTSEEN_TIMEOUT,
                )
        except AttributeError:
            pass
