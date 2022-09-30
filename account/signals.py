from django.db.models.signals import post_save, pre_save
from hashlib import md5
from random import randint
from django.dispatch import receiver
from django.core.mail import send_mail
from config import settings
import datetime

import account.models
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
def password_reset_code_maker(sender, instance, created, **kwargs):
    if created:
        try:
            user = User.objects.get(email=instance.email)
            print(user)
            print('voy')
            code = str(randint(1000, 9999))
            hash_code = md5(code.encode()).hexdigest()
            instance.code = hash_code
            instance.user = user
            instance.save()
            send_mail(subject='Salom', message=f'''Hi {instance.user.first_name}!

                                            Your verification code for reset password is {code}.

                                            Enter this code in our website to open password reset options''',
                      from_email=settings.EMAIL_HOST_USER, recipient_list=[instance.email, ])
        except User.DoesNotExist:
            print('iya')
            instance.delete()
