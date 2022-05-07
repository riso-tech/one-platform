from django.urls import path

from one.contrib.auth.contexts.views import group_list_view

app_name = "auth"
urlpatterns = [
    path("", view=group_list_view, name="group-list"),
]
