from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_admin', ]

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (

    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "first_name", "last_name", "password1", "password2"),
            },
        ),
    )
