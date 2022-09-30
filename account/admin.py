from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account import models


class UserSettingItemInline(admin.TabularInline):
    model = models.UserSetting
    raw_id_fields = ['user']


admin.site.register(models.LanguageSetting)


@admin.register(models.PasswordRecoveryCode)
class PasswordRecoveryCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'valid_from', 'valid_to']
    readonly_fields = ['code', 'valid_from', 'valid_to', 'user']

    fieldsets = (
        (None, {
            'fields': ('user', 'valid_from', 'valid_to', 'code')
        }),
    )


@admin.register(models.PasswordRecoveryLink)
class PasswordRecoveryLinkAdmin(admin.ModelAdmin):
    list_display = ['user', 'valid_from', 'valid_to']
    readonly_fields = ['link', ]


@admin.register(models.User)
class UserAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_admin', ]
    inlines = [UserSettingItemInline]

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login",)}),
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
