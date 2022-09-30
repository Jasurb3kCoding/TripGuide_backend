from django.db.models.signals import post_save, pre_save
from hashlib import md5
from random import randint
from django.dispatch import receiver
from django.core.mail import send_mail
from config import settings
import datetime
from django.utils import timezone
from config import settings

import account.models
from account.models import User, UserSetting, UserVerificationCode


@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        instance.username = instance.email
        instance.save()
        UserSetting.objects.create(user=instance)
        code = str(randint(1000, 9999))
        hash_code = md5(code.encode()).hexdigest()
        UserVerificationCode.objects.create(email=instance.email,
                                            code=hash_code,
                                            user=instance,
                                            valid_to=timezone.now() + datetime.timedelta(
                                                seconds=settings.PASSWORD_RECOVERY_HASH_LIFETIME))
        send_mail(subject='You’re almost done!', message=f''' Hi {instance.first_name}
                                                Your verification code is {code}.
                                                
                                                Enter this code in our web site to activate your account.
                                                
                                                If you have any questions, send us an email {settings.EMAIL_HOST_USER}.
                                                
                                                We’re glad you’re here!
                                                The TripGuide team''',
                  from_email=settings.EMAIL_HOST_USER, recipient_list=[instance.email, ])

    else:
        if instance.email != instance.username:
            instance.username = instance.email
            instance.save()
