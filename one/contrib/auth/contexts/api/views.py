from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from one.components.viewsets import BaseModelViewSet
from one.contrib.auth.contexts.api.serializers import GroupSerializer


class GroupViewSet(BaseModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_fields = [
        {
            "key": "group",
            "label": _("Group"),
            "data_label": "name",
            "data_value": "pk",
            "model": Group,
        }
    ]
