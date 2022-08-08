from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Класс определения политики доступа."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
