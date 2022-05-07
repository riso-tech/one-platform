from django.core.exceptions import FieldDoesNotExist
from django.db.models import F
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class BaseModelViewSet(ModelViewSet):
    """
    Custom ModelViewSet
    """

    def get_model(self):
        """return model of class"""
        return self.serializer_class.Meta.model

    def field_exist(self, field):
        """
        Check if field exist in model
        :param field:
        :return:
        """
        try:
            field = self.get_model()._meta.get_field(field)
        except FieldDoesNotExist:
            return False
        if field.is_relation:
            return False
        return True

    def is_protected(self):
        """Check if model have is_protect field"""
        return self.field_exist("is_protected")

    @action(detail=False, methods=["get"], url_path="get-choices")
    def get_choices(self, request, *args, **kwargs):
        """
        Return choice for field
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        field = request.GET.get("field")
        if not field or not self.field_exist(field):
            return Response(data=[])

        return Response(
            data={
                "results": self.get_model()
                .objects.all()
                .annotate(name=F(f"{field}"))
                .values(field, "name")
                .distinct()
            }
        )

    @action(detail=False, methods=["delete"])
    def delete(self, request, *args, **kwargs):
        """
        Delete list
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instances = self.queryset.filter(pk__in=request.data)
        if self.is_protected():
            instances = instances.filter(is_protected=False)
        instances.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
