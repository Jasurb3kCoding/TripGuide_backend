from django.db.models.signals import post_save, pre_save
from django.contrib.auth.hashers import make_password
from random import randint
from django.dispatch import receiver
import datetime
from account.models import User, UserSetting, PasswordRecoveryCode


@receiver(post_save, sender=User)
def username_filler(sender, instance, created, **kwargs):
    if created:
        instance.username = instance.email
        UserSetting.objects.create(user=instance)
        instance.save()
    else:
        if instance.email != instance.username:
            instance.username = instance.email
            instance.save()


@receiver(post_save, sender=PasswordRecoveryCode)
def code_maker(sender, instance, created, **kwargs):
    if created:
        print(instance)
        code = str(randint(1000, 9999))
        hash_code = make_password(code)
        instance.code = hash_code
        instance.save()
