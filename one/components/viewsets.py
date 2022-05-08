from django.core.exceptions import FieldError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from one.utils.data_processing import getattr_in_chain


class BaseModelViewSet(ModelViewSet):
    """
    Custom ModelViewSet
    """

    filter_fields = []

    def get_options(self):
        return "options", [
            {
                "key": item["key"],
                "label": item["label"],
                "data": [
                    {
                        "label": getattr_in_chain(obj, item["data_label"]),
                        "value": getattr_in_chain(obj, item["data_value"]),
                    }
                    for obj in item["model"].objects.all()
                ],
            }
            for item in self.filter_fields
        ]

    class Meta:
        datatables_extra_json = ("get_options",)

    def get_model(self):
        """return model of class"""
        return self.serializer_class.Meta.model

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
        # try:
        #     meta = getattr(self.get_model(), "Metadata", None)
        #     if meta:
        #         instances = instances.filter(**{f"{meta.protect_flag_field}": False})
        # except FieldError:
        #     pass
        try:
            instances = instances.filter(is_protected=False)
        except FieldError:
            pass
        instances.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
