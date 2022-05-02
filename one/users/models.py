import datetime
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.db.models import CharField, UUIDField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from one.components.models import BaseModel


class User(BaseModel, AbstractUser):
    """
    Default custom user model for Riso Tech one platform.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    language = CharField(
        _("User default language"),
        max_length=2,
        choices=settings.LANGUAGES,
        default=settings.ENGLISH,
    )
    theme = CharField(
        _("User default theme"),
        max_length=5,
        choices=settings.THEMES,
        default=settings.LIGHT_THEME,
    )

    class Metadata:
        avatar_field = None
        name_field = "name"
        title_field = None

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    # User Online Status
    @property
    def last_seen(self):
        """last online at"""
        return cache.get("seen_%s" % self.username)

    @property
    def is_online(self):
        """Is online at least before timeout"""
        if not self.last_seen:
            return False
        now = datetime.datetime.now()
        _is_online = now > self.last_seen + datetime.timedelta(
            seconds=settings.USER_ONLINE_TIMEOUT
        )
        return not _is_online

    @property
    def is_online_dot(self):
        """Is online red dot/ blue dot"""
        online = (
            '<div class="position-absolute translate-middle bottom-0 start-100 mb-6 bg-success'
            + ' rounded-circle border border-4 border-white h-20px w-20px"></div>'
        )

        offline = (
            '<div class="position-absolute translate-middle bottom-0 start-100 mb-6 bg-danger'
            + ' rounded-circle border border-4 border-white h-20px w-20px"></div>'
        )

        return online if self.is_online else offline

    # End User Online Status

    # Constructor Set
    def set_theme(self, theme):
        """Set theme"""
        self.theme = theme
        self.save()

    def set_language(self, language):
        """Set theme"""
        self.language = language
        self.save()

    # End Constructor Set
