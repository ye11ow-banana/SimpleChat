from django.db.models.signals import post_save
from django.dispatch import receiver

from . import services
from .models import Message


@receiver(post_save, sender=Message)
def set_thread_last_update(sender, instance, created, **kwargs):
    if created:
        services.set_thread_last_update(instance.thread_id, instance.created)
