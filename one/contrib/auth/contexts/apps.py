from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _


def create_default_group_context(sender, **kwargs):
    """after migrations"""
    from django.contrib.auth.models import Group

    from .models import Context

    groups = Group.objects.filter()

    for group in groups:
        if not Context.objects.filter(group=group).exists():
            Context.objects.create(group=group)


class GroupConfig(AppConfig):
    name = "one.contrib.auth.contexts"
    verbose_name = _("Groups")

    def ready(self):
        post_migrate.connect(create_default_group_context, sender=self)
        from .signals import create_or_update_group_context  # noqa
