import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView

from .forms import ContextForm


class GroupListView(LoginRequiredMixin, ListView):
    model = Group

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs["breadcrumb"] = {
            "title": _("Group List"),
            "parent": None,
            "current": _("List of Group"),
        }
        kwargs["context_form"] = ContextForm()
        return kwargs


group_list_view = GroupListView.as_view()


class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):  # noqa
        return reverse("auth:group-list")

    def form_valid(self, form):
        self.object = form.save()  # noqa
        context_form = ContextForm(
            self.request.POST, self.request.FILES, instance=self.object.context
        )
        if context_form.is_valid():
            context_form.save()
        else:
            errors = json.loads(context_form.errors.as_json())
            if errors:
                for error in errors:
                    messages.error(self.request, errors[error][0]["message"])
            self.object.delete()
        return redirect(self.get_success_url())


group_create_view = GroupCreateView.as_view()
