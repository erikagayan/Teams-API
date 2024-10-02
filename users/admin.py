from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Определение модели администрирования для пользовательской модели User."""
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "team")}),
        (
            _("Permissions"),
            {"fields": ("is_moderator", "is_manager", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2", "is_moderator", "is_manager", "team"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_moderator", "is_manager", "is_staff")
    list_filter = ("is_moderator", "is_manager", "is_staff", "is_superuser")
    search_fields = ("email", "first_name", "last_name", "username")
    ordering = ("email",)
