from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _


def create_default_site_setting(sender, **kwargs):
    """after migrations"""
    from django.contrib.sites.models import Site

    from .models import Setting

    site = Site.objects.get(id=getattr(settings, "SITE_ID", 1))

    if not Setting.objects.exists():
        Setting.objects.create(site=site)


class SiteConfig(AppConfig):
    name = "one.contrib.sites.settings"
    verbose_name = _("Sites")

    def ready(self):
        post_migrate.connect(create_default_site_setting, sender=self)
        from .signals import create_or_update_site_setting  # noqa
