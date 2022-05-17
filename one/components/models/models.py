from random import randint
from uuid import uuid4

from django.conf import settings
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    UUIDField,
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ModelSerializer

from .managers import LingualManager


class MetaModel(Model):
    class Meta:
        abstract = True

    class Metadata:
        avatar_field = None
        name_field = None
        title_field = None
        protect_flag_field = None

    @property
    def as_avatar(self):
        """Return object as Image url instead of __str__"""
        avatar = getattr(self, str(self.Metadata.avatar_field), None)
        return (
            f"/static/metronic/media/svg/shapes/abstract-{randint(1, 5)}-dark.svg"
            if not avatar
            else getattr(avatar, "url")
        )

    @property
    def as_name(self):
        """Return object as value of name field instead of __str__"""
        name = getattr(self, str(self.Metadata.name_field), None)
        return name if name else str(self)

    @property
    def as_title(self):
        """Return object as value of title field instead of __str__"""
        name = getattr(self, str(self.Metadata.title_field), None)
        return name if name else ""

    @property
    def as_choice(self):
        """Render object as image and name in choice"""
        image = "<img class='rounded-circle me-2' src='{self.as_avatar}' style='width: 26px;'>"
        return f"<span>{image}{self.as_name}</span>"

    @property
    def as_cell(self):
        """
        Render object as image and name and title in table cell
        """
        return (
            '<div class="d-flex align-items-center">'
            + '<div class="symbol symbol-45px me-5">'
            + f'<img alt="{self.as_name}" src="{self.as_avatar}">'
            + "</div>"
            + '<div class="d-flex justify-content-start flex-column">'
            + '<a href="#" class="text-dark fw-bolder text-hover-primary '
            + f'mb-1 fs-6">{self.as_name}</a>'
            + f'<span class="text-muted fw-bold text-muted d-block fs-7">{self.as_title}</span>'
            + "</div>"
            + "</div>"
        )

    @property
    def as_dict(self):
        """as_dict"""

        class ObjectSerializer(ModelSerializer):
            class Meta:
                model = type(self)
                fields = "__all__"
                depth = 1

        serializer = ObjectSerializer(self)
        return [
            {"key": item, "value": serializer.data.get(item)}
            for item in serializer.data
        ]


class BaseModel(MetaModel):
    """
    Abstract Base model

    id: UUIDField, random UUID
    time_created: DateTimeField, Created time of object
    time_modified: DateTimeField, Last modified time of object
    creator: User, created by
    last_modified_by: User, Last modified by
    """

    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    time_created = DateTimeField(
        verbose_name=_("Created on"), auto_now_add=True, null=True
    )
    time_modified = DateTimeField(
        verbose_name=_("Last modified on"), auto_now=True, null=True
    )
    creator = ForeignKey(
        "users.User",
        verbose_name=_("Created by"),
        related_name="%(app_label)s_%(class)s_creator",
        null=True,
        blank=True,
        on_delete=CASCADE,
    )
    last_modified_by = ForeignKey(
        "users.User",
        verbose_name="Last modified by",
        related_name="%(app_label)s_%(class)s_last_modified_by",
        null=True,
        blank=True,
        on_delete=CASCADE,
    )

    class Meta:
        """Meta override abstract"""

        abstract = True

    def save(self, *args, **kwargs):
        """
        Auto update time_modified
        :param args:
        :param kwargs:
        :return:
        """
        if not self.time_created:
            self.time_created = timezone.now()

        self.time_modified = timezone.now()
        return super().save(*args, **kwargs)


class LingualModel(BaseModel):
    """
    Abstract Multi language Model

    language: CharField, language of object
    """

    language = CharField(
        max_length=2,
        verbose_name=_("Language"),
        choices=settings.LANGUAGES,
        default=settings.VIETNAMESE,
    )
    lingual_objects = LingualManager()

    class Meta:
        abstract = True

    @property
    def language_verbose(self):
        return dict(settings.LANGUAGES)[self.language]
