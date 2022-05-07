from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from one.contrib.auth.contexts.api.views import GroupViewSet
from one.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("groups", GroupViewSet)

app_name = "api"
urlpatterns = router.urls
