from django.urls import path
from django.views.generic import RedirectView

from one.pages.views import RenderView

app_name = "pages"
urlpatterns = [
    path("", RenderView.as_view(), name="home"),
    path("<slug:slug>", RenderView.as_view(), name="slug"),
    path("<slug:slug>/", RedirectView.as_view(pattern_name="pages:slug")),
]
