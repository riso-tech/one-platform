from django.urls import path

from one.contrib.sites.settings.views import site_detail_view

app_name = "settings"
urlpatterns = [path("", view=site_detail_view, name="site")]
