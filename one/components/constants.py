"""
Base Constants
"""
from django.forms.fields import (
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    DurationField,
    EmailField,
    FileField,
    FloatField,
    GenericIPAddressField,
    ImageField,
    IntegerField,
    JSONField,
    NullBooleanField,
    SlugField,
    TimeField,
    TypedChoiceField,
    URLField,
    UUIDField,
)
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView, UpdateView

EXCLUDE_FIELDS = ["password"]

FORM_LAYOUT_1_COL = "1COL"
FORM_LAYOUT_2_COL = "2COL"

FORM_LAYOUTS = (
    (FORM_LAYOUT_1_COL, _("One column")),
    (FORM_LAYOUT_2_COL, _("Two column")),
)

CLASS_DANGER = "danger"
CLASS_WARNING = "warning"
CLASS_SUCCESS = "success"
CLASS_INFO = "info"
CLASS_PRIMARY = "primary"
CLASS_DARK = "dark"

CLASS_COLOR = (
    (CLASS_DANGER, _("Red")),
    (CLASS_WARNING, _("Yellow")),
    (CLASS_SUCCESS, _("Green")),
    (CLASS_INFO, _("Purple")),
    (CLASS_PRIMARY, _("Blue")),
    (CLASS_DARK, _("Black")),
)

# noinspection name
ACTION_LIST = ListView
# noinspection name
ACTION_VIEW = DetailView
# noinspection name
ACTION_UPDATE = UpdateView

ACTION_DICT = (
    (ACTION_LIST, _("(Action) List")),
    (ACTION_VIEW, _("(Action) View")),
    (ACTION_UPDATE, _("(Action) Update")),
)

FIELD_TYPE_DICT = (
    (CharField, "TEXT"),
    (CharField, "TEXT"),
    (DateField, "DATE"),
    (DateTimeField, "DATETIME"),
    (TimeField, "TIME"),
    (ImageField, "IMAGE"),
    (FileField, "FILE"),
    (BooleanField, "SWITCH"),
    (NullBooleanField, "NULLSWITCH"),
    (ModelMultipleChoiceField, "MULTICHOICE"),
    (ModelChoiceField, "CHOICE"),
    (TypedChoiceField, "CHOICE"),
    (DecimalField, "NUMBER"),
    (FloatField, "NUMBER"),
    (IntegerField, "NUMBER"),
    (DurationField, "RANGE"),
    (EmailField, "EMAIL"),
    (GenericIPAddressField, "IP"),
    (JSONField, "JSON"),
    (SlugField, "SLUG"),
    (UUIDField, "SLUG"),
    (URLField, "URL"),
)
