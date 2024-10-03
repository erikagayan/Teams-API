from rest_framework import permissions


def is_admin_moderator_manager(user):
    if not user.is_authenticated:
        return False
    return (
        user.is_superuser
        or getattr(user, "is_moderator", False)
        or getattr(user, "is_manager", False)
    )


class IsAdminModeratorManager(permissions.BasePermission):
    """
    A user permission that allows only administrators,
    moderators and managers to perform any actions.
    Other users have read-only privileges.
    """

    def has_permission(self, request, view):
        # Allow secure methods (GET, HEAD, OPTIONS) to all
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow unsafe methods for administrators, moderators and managers only
        return is_admin_moderator_manager(request.user)

    def has_object_permission(self, request, view, obj):
        # Apply the same rules at the object level
        if request.method in permissions.SAFE_METHODS:
            return True
        return is_admin_moderator_manager(request.user)
