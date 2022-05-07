from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from webpush.models import Group as PushGroup

from .models import Context


@receiver(post_save, sender=Group)
def create_or_update_group_context(sender, instance, **kwargs):
    """This signal creates/updates a Setting object
    after creating/updating a Site object.
    """
    context, created = Context.objects.update_or_create(group=instance)
    if not created:
        context.save()
    PushGroup.objects.update_or_create(name=instance.name)
