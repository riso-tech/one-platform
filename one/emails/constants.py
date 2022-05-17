from django.utils.translation import gettext_lazy as _

TEMPLATE_SIGNUP = "allauth_signup"
TEMPLATE_RESET = "allauth_reset"
TEMPLATE_CONFIRM = "allauth_confirm"
TEMPLATE_UNKNOWN = "allauth_unknown"

ALLAUTH_TEMPLATES = (
    (TEMPLATE_SIGNUP, _("allauth_signup")),
    (TEMPLATE_RESET, _("allauth_reset")),
    (TEMPLATE_CONFIRM, _("allauth_confirm")),
    (TEMPLATE_UNKNOWN, _("allauth_unknown")),
)
