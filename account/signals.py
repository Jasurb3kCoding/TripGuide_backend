from django.db.models.signals import post_save

from django.dispatch import receiver
from account.models import User, UserSetting


@receiver(post_save, sender=User)
def username_filler(sender, instance, created, **kwargs):
    if created:
        instance.username = instance.email
        UserSetting.objects.create(user=instance)
        instance.save()
