from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define the administration model for the User user model."""

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "team")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_moderator",
                    "is_manager",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "is_moderator",
                    "is_manager",
                    "team",
                ),
            },
        ),
    )
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_moderator",
        "is_manager",
        "is_staff",
    )
    list_filter = ("is_moderator", "is_manager", "is_staff", "is_superuser")
    search_fields = ("email", "first_name", "last_name", "username")
    ordering = ("email",)

    def has_delete_permission(self, request, obj=None):
        """Prohibits managers from removing moderators and administrators."""
        if not request.user.is_superuser:
            if obj is not None:
                if obj.is_superuser or obj.is_moderator:
                    return False  # Managers cannot remove moderators and administrators
        return super().has_delete_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        """Prohibits managers from editing moderators and administrators."""
        if not request.user.is_superuser:
            if obj is not None:
                if obj.is_superuser or obj.is_moderator:
                    return False  # Managers cannot change moderators and administrators
        return super().has_change_permission(request, obj)

    def get_queryset(self, request):
        """Managers can't see superusers and moderators."""
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_moderator:
            return qs
        # Filter superusers and moderators from the list for managers
        return qs.filter(is_superuser=False, is_moderator=False)

    def get_form(self, request, obj=None, **kwargs):
        """Restricts managers from changing certain fields."""
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            # Limit the fields that the manager can modify
            disabled_fields = {
                "is_superuser",
                "is_staff",
                "is_moderator",
                "groups",
                "user_permissions",
            }
            for field in disabled_fields:
                if field in form.base_fields:
                    form.base_fields[field].disabled = True
        return form
