from django.contrib.auth.models import Group
from django.db.models import CASCADE, ImageField, Model, OneToOneField
from django.utils.translation import gettext_lazy as _

from .utils import group_context_images_directory_path


class Context(Model):
    """Setting model is OneToOne related to Site model."""

    group = OneToOneField(
        Group,
        on_delete=CASCADE,
        primary_key=True,
        related_name="context",
        verbose_name="group",
    )

    avatar = ImageField(
        _("Avatar of group"),
        blank=True,
        null=True,
        upload_to=group_context_images_directory_path,
    )

    def __str__(self):
        return self.group.name

    @property
    def avatar_url(self):
        """Return logo url"""
        return (
            "/static/metronic/media/logos/logo-1-dark.svg"
            if not self.avatar
            else getattr(self.avatar, "url")
        )
