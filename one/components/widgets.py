"""
Override Widgets
"""
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField


class LabelModelChoiceField(ModelChoiceField):
    """Update label of choice with image"""

    def label_from_instance(self, obj):
        """:return choice in html or string"""
        if hasattr(obj, "display_choice_html"):
            return obj.display_choice_html
        return str(obj)


class LabelModelMultipleChoiceField(LabelModelChoiceField, ModelMultipleChoiceField):
    """Update label of choice with image"""
