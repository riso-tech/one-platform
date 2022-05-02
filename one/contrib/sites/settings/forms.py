from django.forms import ModelForm

from .models import Setting


class SettingForm(ModelForm):
    class Meta:
        model = Setting
        fields = "__all__"
