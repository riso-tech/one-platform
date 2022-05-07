from django.contrib.auth.models import Group

from one.components.viewsets import BaseModelViewSet
from one.contrib.auth.contexts.api.serializers import GroupSerializer


class GroupViewSet(BaseModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
