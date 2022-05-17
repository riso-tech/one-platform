from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EmailsConfig(AppConfig):
    """
    AppConfig of emails module
    """

    name = "one.emails"
    verbose_name = _("Emails")

    def ready(self):
        pass
