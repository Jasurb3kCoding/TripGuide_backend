from django.db.models.signals import post_save

from django.dispatch import receiver
from account.models import User


@receiver(post_save, sender=User)
def username_filler(sender, instance, created, **kwargs):
    if created:
        instance.username = instance.email
        instance.save()
