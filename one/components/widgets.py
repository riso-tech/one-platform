"""
Override Widgets
"""
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField


class LabelModelChoiceField(ModelChoiceField):
    """Update label of choice with image"""

    def label_from_instance(self, obj):
        """:return choice in html or string"""
        return obj.as_choice if hasattr(obj, "as_choice") else str(obj)


class LabelModelMultipleChoiceField(LabelModelChoiceField, ModelMultipleChoiceField):
    """Update label of choice with image"""
