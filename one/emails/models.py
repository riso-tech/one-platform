from django.db.models import BooleanField, CharField, TextField
from django.utils.translation import gettext_lazy as _

from one.components.models.models import LingualModel
from one.emails.constants import ALLAUTH_TEMPLATES


class AllauthTemplate(LingualModel):
    """
    Email template for reuse

    code: CharField, Specific code for core app
    subject: CharField, Email title
    is_protected: BooleanField, can delete or not
    content: TextField, html content
    """

    code = CharField(
        _("Specific code for core app"),
        max_length=50,
        blank=True,
        null=True,
        editable=False,
        choices=ALLAUTH_TEMPLATES,
    )
    subject = CharField(_("Subject of email"), max_length=1000, blank=True, null=True)
    is_protected = BooleanField(_("Is protected"), default=False)
    content = TextField(_("Html content"))

    class Meta:
        permissions = [
            ("list_allauthtemplate", "Can list allauth email template"),
        ]
        unique_together = (
            "code",
            "language",
        )
