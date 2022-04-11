"""
User Views
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView

from one.components.constants import FORM_LAYOUT_2_COL
from one.components.views import ExposeUpdateView

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    """UserDetailView"""

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, ExposeUpdateView):
    """UserUpdateView"""

    model = User
    fields = ["username", "name"]
    success_message = _("Information successfully updated")
    layout = FORM_LAYOUT_2_COL
    read_only_fields = ["username"]

    def get_success_url(self):
        """get_success_url"""
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        """get_object"""
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    """UserRedirectView"""

    permanent = False

    def get_redirect_url(self):
        """get_redirect_url"""
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
