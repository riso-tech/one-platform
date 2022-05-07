from django.contrib.auth.models import Group
from rest_framework.serializers import ModelSerializer

from one.contrib.auth.contexts.models import Context


class ContextSerializer(ModelSerializer):
    class Meta:
        model = Context
        fields = ["as_cell"]


class GroupSerializer(ModelSerializer):
    context = ContextSerializer()

    class Meta:
        model = Group
        fields = ["id", "name", "context"]
