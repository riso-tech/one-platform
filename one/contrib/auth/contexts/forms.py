from django.forms import ModelForm

from .models import Context


class ContextForm(ModelForm):
    class Meta:
        model = Context
        exclude = ["group"]
