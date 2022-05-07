from django.contrib.auth.models import Group
from rest_framework.viewsets import ModelViewSet

from one.contrib.auth.contexts.api.serializers import GroupSerializer


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
