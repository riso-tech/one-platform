from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Setting


@receiver(post_save, sender=Site)
def create_or_update_site_setting(sender, instance, **kwargs):
    """This signal creates/updates a Setting object
    after creating/updating a Site object.
    """
    setting, created = Setting.objects.update_or_create(site=instance)
    if not created:
        setting.save()
