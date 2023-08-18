from django.db.models.signals import post_save
from django.dispatch import receiver
from cashdeskapp.models import Enterprise
from .context_processors import update_global_context_variable


@receiver(post_save, sender=Enterprise)
def update_global_context(sender, instance, **kwargs):
    update_global_context_variable(instance)
