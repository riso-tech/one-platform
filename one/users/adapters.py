from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_display
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpRequest

from one.emails.constants import (
    TEMPLATE_CONFIRM,
    TEMPLATE_RESET,
    TEMPLATE_SIGNUP,
    TEMPLATE_UNKNOWN,
)
from one.emails.utils import context_render_from_template
from one.utils.requests import RequestProcess


class AccountAdapter(DefaultAccountAdapter):
    """
    AllAuth Override Normal Adapter
    """

    def is_open_for_signup(self, request: HttpRequest):
        """Allow new user registration new account"""
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def render_mail(self, template_prefix, email, context, headers=None):
        """
        Renders an e-mail to `email`.  `template_prefix` identifies the
        e-mail that is to be sent, e.g. "account/email/email_confirmation"
        """
        from_email = self.get_from_email()

        requests_process = RequestProcess(self.request)
        context["host"] = requests_process.host()
        context["user_display"] = user_display(context["user"])

        subjects = {
            "account/email/email_confirmation_signup": TEMPLATE_SIGNUP,
            "account/email/password_reset_key": TEMPLATE_RESET,
            "account/email/email_confirmation": TEMPLATE_CONFIRM,
            "account/email/unknown_account": TEMPLATE_UNKNOWN,
        }

        subject_context = {}

        mail_type = subjects[template_prefix]

        subject, bodies = context_render_from_template(
            mail_type, context, subject_context, requests_process.language_code()
        )

        msg = EmailMessage(subject.strip(), bodies, from_email, [email])
        msg.content_subtype = "html"  # Main content is now text/html
        return msg


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    AllAuth Override Social Adapter
    """

    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        """Allow new user registration new account using social account"""
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
