from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, UpdateView

from .forms import ContextForm


class GroupListView(LoginRequiredMixin, ListView):
    model = Group


group_list_view = GroupListView.as_view()


class GroupUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Group
    fields = ["name", "permissions"]
    success_message = _("Information successfully updated")

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs["breadcrumb"] = {
            "title": _("Group Context"),
            "parent": None,
            "current": f"{_('Update for')} {self.object.name}",
        }
        if self.request.method == "POST":
            kwargs["context_form"] = ContextForm(
                self.request.POST, self.request.FILES, instance=self.object.context
            )
        else:
            kwargs["context_form"] = ContextForm(instance=self.object.context)
        return kwargs

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = self.get_object()
        context_form = ContextForm(
            self.request.POST, self.request.FILES, instance=self.object.context
        )
        form = self.get_form()
        if form.is_valid():
            if context_form.is_valid():
                self.form_valid(context_form)
                return self.form_valid(form)
        messages.error(request, _("Step Images has error"))
        return self.form_invalid(form)


group_update_view = GroupUpdateView.as_view()
