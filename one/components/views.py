"""
Base Views
"""
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from django.http import Http404
from django.urls import NoReverseMatch, reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView, UpdateView

from one.components.constants import ACTION_DICT, FIELD_TYPE_DICT, FORM_LAYOUT_1_COL
from one.components.utils import _get_fields, _get_lookups
from one.components.widgets import LabelModelChoiceField, LabelModelMultipleChoiceField


class ExtendView:
    """Add custom function for View"""

    model = None

    def breadcrumb(self):
        """
        List of breadcrumb object
        :return:
        """
        # noinspection PyProtectedMember
        model_meta = self.model._meta
        title = _(model_meta.verbose_name_plural.title())
        type_view = ListView
        object_name = ""
        parent = None

        try:
            assert self.object
            title = _(model_meta.verbose_name.title())
            type_view = DetailView
            object_name = self.object

            user = self.request.user
            if any(
                [
                    user.is_superuser,
                    user.has_perm(
                        f"{model_meta.app_label}.view_{model_meta.verbose_name}"
                    ),
                ]
            ):
                try:
                    parent = reverse(f"{model_meta.app_label}:list")
                except NoReverseMatch:
                    try:
                        parent = reverse(f"{model_meta.verbose_name_plural}:list")
                    except NoReverseMatch:
                        parent = None

        except AttributeError:
            pass

        try:
            assert self.get_form()
            type_view = UpdateView
        except AttributeError:
            pass

        action = dict(ACTION_DICT)[type_view]

        return {
            "title": title,
            "parent": parent,
            "current": f"{_(action)} {object_name}",
        }

    def get_endpoint(self):
        """Dictionary of default endpoint"""
        # noinspection PyProtectedMember
        model_meta = self.model._meta
        title = model_meta.verbose_name_plural

        return {
            "LIST": reverse(f"api:{title}-list"),
            "DELETE": reverse(f"api:{title}-delete"),
            "CHOICES": reverse(f"api:{title}-get-choices"),
        }

    @staticmethod
    def get_field_value(_object, field):
        """
        Get Value of field from object
        :param _object:
        :param field:
        :return:
        """
        return getattr(_object, field)


class ExposeListView(ExtendView, ListView):
    """Auto add model fields to context of ListView"""

    template_name = "defaults/_list.html"
    object_list = None

    def get(self, request, *args, **kwargs):
        """add model fields to context"""
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(
                self.object_list, "exists"
            ):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(
                    _("Empty list and “%(class_name)s.allow_empty” is False.")
                    % {
                        "class_name": self.__class__.__name__,
                    }
                )

        endpoints = self.get_endpoint()
        context = self.get_context_data()
        context["ENDPOINT"] = endpoints
        # noinspection PyProtectedMember
        model_meta = self.model._meta
        fields = _get_fields(model_meta.get_fields(include_parents=False), ["id"])

        context["fields"] = [
            {
                "col": item.name,
                "verbose": item.verbose_name,
                "type": item.get_internal_type(),
                "lookups": _get_lookups(item),
                "choices": [],
                "choice_url": f"{endpoints['CHOICES']}?field={item.name}",
            }
            for item in fields
        ]

        context["breadcrumb"] = self.breadcrumb()

        return self.render_to_response(context)


class ExposeDetailView(ExtendView, DetailView):
    """Auto add model fields to context of DetailView"""

    object = None

    def get(self, request, *args, **kwargs):
        """add model fields to context"""
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        # noinspection PyProtectedMember
        model_meta = self.model._meta
        fields = _get_fields(model_meta.get_fields(include_parents=False))
        context["fields"] = [
            {
                "col": item.name,
                "verbose": item.verbose_name,
                "value": str(self.get_field_value(self.object, item.name)),
                "type": str(type(item)),
            }
            for item in fields
        ]
        context["breadcrumb"] = self.breadcrumb()
        return self.render_to_response(context)


class ExposeUpdateView(ExtendView, UpdateView):
    """Override context data"""

    read_only_fields = []
    layout = FORM_LAYOUT_1_COL

    @staticmethod
    def field_processing(form):
        """Update field in context"""
        for field in form.fields:
            _field = form.fields[field]
            widget = _field.widget
            attrs = widget.attrs

            attrs.update({"input_type": dict(FIELD_TYPE_DICT)[type(_field)]})

            if hasattr(widget, "input_type") and widget.input_type == "select":
                if isinstance(_field, ModelChoiceField):
                    form.fields[field] = LabelModelChoiceField(_field.queryset)
                elif isinstance(_field, ModelMultipleChoiceField):
                    form.fields[field] = LabelModelMultipleChoiceField(_field.queryset)

    def readonly_field_processing(self, form):
        """Update readonly field in context"""
        for field in self.read_only_fields:
            _field = form.fields[field]
            attrs = _field.widget.attrs
            attrs.update({"readonly": "readonly"})

    def get_context_data(self, **kwargs):
        """Auto add class to form field, and read only field"""
        kwargs = super().get_context_data(**kwargs)
        kwargs["breadcrumb"] = self.breadcrumb()
        kwargs.update({"layout": self.layout})
        form = kwargs["form"]

        self.field_processing(form)
        self.readonly_field_processing(form)
        return kwargs
