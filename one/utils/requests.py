from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

User = get_user_model()


class RequestProcess:
    """
    Class to process request
    """

    def __init__(self, request):
        """initial"""
        self.request = request
        self.current_site = get_current_site(request)

    def protocol(self):
        """:return protocol of request"""
        return "https://" if self.request.is_secure() else "http://"

    def host(self):
        """:return host = protocol + domain"""
        return "{0}{1}".format(self.protocol(), self.current_site.domain)

    def lazy_user(self):
        """:return lazy user"""
        return self.request.user

    def user(self):
        """:return user"""
        return User.objects.get(pk=self.request.user.id)

    def language_code(self):
        """:return request language code"""
        return self.request.LANGUAGE_CODE.lower()
