from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView


class GroupListView(LoginRequiredMixin, ListView):
    model = Group

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs["breadcrumb"] = {
            "title": _("Group List"),
            "parent": None,
            "current": _("List of Group"),
        }
        return kwargs


group_list_view = GroupListView.as_view()
