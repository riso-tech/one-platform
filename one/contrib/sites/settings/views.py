from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.models import Site
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView

from .forms import SettingForm


class SiteDetailView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Site
    fields = ["name", "domain"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return reverse("settings:site")

    def get_object(self):
        return Site.objects.get_current()

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs["breadcrumb"] = {
            "title": _("Site Setting"),
            "parent": None,
            "current": f"{_('Update for')} {self.object.name}",
        }
        if self.request.method == "POST":
            kwargs["setting_form"] = SettingForm(
                self.request.POST, self.request.FILES, instance=self.object.setting
            )
        else:
            kwargs["setting_form"] = SettingForm(instance=self.object.setting)
        return kwargs

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = self.get_object()
        setting_form = SettingForm(
            self.request.POST, self.request.FILES, instance=self.object.setting
        )
        form = self.get_form()
        if form.is_valid():
            if setting_form.is_valid():
                self.form_valid(setting_form)
                return self.form_valid(form)
        messages.error(request, _("Step Images has error"))
        return self.form_invalid(form)


site_detail_view = SiteDetailView.as_view()
