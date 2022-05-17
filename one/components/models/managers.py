# from django.conf import settings
from django.db.models import Manager
from django.forms import modelform_factory

# from django.forms import modelformset_factory, modelform_factory, HiddenInput
# from django.utils.translation import activate, get_language


# def readonly_field_processing(form, read_only_fields):
#     """Update readonly field in context"""
#     if read_only_fields:
#         for field in read_only_fields:
#             _field = form.fields[field]
#             attrs = _field.widget.attrs
#             attrs.update({"readonly": "readonly"})


# def hidden_field_processing(form, hidden_fields):
#     """Update readonly field in context"""
#     if hidden_fields:
#         for field in hidden_fields:
#             _field = form.fields[field]
#             _field.widget = HiddenInput()


class FormManager(Manager):
    def get_form_class(self):
        """get form class
        :rtype: ModelForm
        """
        model = self.model
        form_meta = getattr(model, "FormMeta", None)
        fields = "__all__"
        exclude_fields = None
        if form_meta:
            fields = (
                form_meta.fields if getattr(form_meta, "fields", None) else "__all__"
            )
            exclude_fields = getattr(form_meta, "exclude_fields")
        return modelform_factory(model=model, fields=fields, exclude=exclude_fields)

    # def get_formset_class(self, **kwargs):
    #     """get formset class"""
    #     return modelformset_factory(
    #         model=self.model, form=self.get_form_class(), **kwargs
    #     )

    # def as_formset(self, queryset=None, **kwargs):
    #     _formset = self.get_formset_class(**kwargs)
    #     queryset = queryset if queryset else self.get_queryset()
    #     formset = _formset(queryset=queryset)
    #     model = self.model
    #     form_meta = getattr(model, "FormMeta", None)
    #     if form_meta:
    #         read_only_fields = getattr(form_meta, "read_only_fields", None)
    #         hidden_fields = getattr(form_meta, "hidden_fields", None)
    #         for form in formset:
    #             readonly_field_processing(form, read_only_fields)
    #             hidden_field_processing(form, hidden_fields)
    #     return formset


# class LingualManager(Manager):
#     def get_queryset_by_language(self, language, order_by=None):
#         query_set = super().get_queryset().filter(language=language)
#         return query_set if not order_by else query_set.order_by(order_by)
#
#     def group_by_language(self, order_by=None):
#         response = []
#         activate(get_language())
#         for language in settings.LANGUAGES:
#             response.append(
#                 {
#                     "language": language[0],
#                     "label": language[1],
#                     "data": self.get_queryset_by_language(
#                         language=language[0], order_by=order_by
#                     ),
#                 }
#             )
#         return response
