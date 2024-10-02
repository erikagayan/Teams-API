from rest_framework import permissions


def is_admin_moderator_manager(user):
    return user.is_superuser or user.is_moderator or user.is_manager


class IsAdminModeratorManager(permissions.BasePermission):
    """
    Пользовательское разрешение, позволяющее только администраторам,
    модераторам и менеджерам выполнять любые действия.
    Другие пользователи имеют только права на чтение.
    """

    def has_permission(self, request, view):
        # Разрешить безопасные методы (GET, HEAD, OPTIONS) всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешить небезопасные методы только администраторам, модераторам и менеджерам
        return is_admin_moderator_manager(request.user)

    def has_object_permission(self, request, view, obj):
        # Применяем те же правила на уровне объекта
        if request.method in permissions.SAFE_METHODS:
            return True
        return is_admin_moderator_manager(request.user)
