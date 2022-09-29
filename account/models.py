from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from base.validators import phone_number_validator
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have an email.')
        if not first_name:
            raise ValueError('Users must have first name.')
        if not last_name:
            raise ValueError('Users must have last name.')
        user = self.model(
            email=self.normalize_email(email),
            username=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name, last_name):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user.save(using=self._db)
        return user


class VerifiedManager(models.Manager):
    def get_queryset(self):
        return super(VerifiedManager, self).get_queryset().filter(is_verified=True)


def get_profile_image_path(self, filename):
    return f'profile_images/{self.id}.png'


def get_background_image_path(self, filename):
    return f'profile_background_images/{self.id}.png'


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(unique=True, null=True, max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)
    profile_photo = models.ImageField(upload_to=get_profile_image_path, blank=True, null=True)
    background_photo = models.ImageField(upload_to=get_background_image_path, blank=True, null=True)
    phone_number = models.CharField(validators=[phone_number_validator], max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()
    verified = VerifiedManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin


class LanguageSetting(models.Model):
    title = models.CharField(max_length=255)
    short_code = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class UserSetting(models.Model):
    user = models.OneToOneField(User,
                                related_name='settings',
                                on_delete=models.CASCADE)
    language = models.ForeignKey(LanguageSetting,
                                 related_name='selected_users',
                                 on_delete=models.SET_NULL,
                                 null=True)
    is_24_system = models.BooleanField(default=True)

    def __str__(self):
        return f'Setting for user {self.user.email}'


class PasswordRecoveryCode(models.Model):
    user = models.ForeignKey(User,
                             related_name='recovered_password_codes',
                             on_delete=models.CASCADE)
    code = models.CharField(max_length=255)
    valid_from = models.DateTimeField(auto_now_add=True)
    valid_to = models.DateTimeField()

    def __str__(self):
        return f'Code for {self.user.email}'

    def is_valid(self):
        return self.valid_from <= timezone.now() <= self.valid_to


class PasswordRecoveryLink(models.Model):
    user = models.ForeignKey(User,
                             related_name='recovered_password_links',
                             on_delete=models.CASCADE)
    link = models.CharField(max_length=255)
    valid_from = models.DateTimeField(auto_now_add=True)
    valid_to = models.DateTimeField()

    def __str__(self):
        return f'Link for {self.user.email}'

    def is_valid(self):
        return self.valid_from <= timezone.now() <= self.valid_to
