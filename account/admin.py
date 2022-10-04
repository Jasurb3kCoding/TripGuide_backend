from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account import models


class UserSettingItemInline(admin.TabularInline):
    model = models.UserSetting
    raw_id_fields = ['user']


@admin.register(models.User)
class UserAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_admin', ]
    inlines = [UserSettingItemInline]

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"),
         {"fields": ("first_name", "last_name", "email", "phone_number", "profile_photo", "background_photo")}),
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


admin.site.register(models.LanguageSetting)


@admin.register(models.UserVerificationCode)
class UserVerificationCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'valid_from', 'valid_to']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        return list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))

    fieldsets = (
        (None, {
            'fields': ('user', 'valid_from', 'valid_to', 'code', 'email')
        }),
    )


@admin.register(models.PasswordRecoveryLink)
class PasswordRecoveryLinkAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        return list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))

    fieldsets = (
        (None, {
            'fields': ('user', 'valid_from', 'valid_to', 'link', 'email', 'uid', 'expired')
        }),
    )
