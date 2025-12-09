from rest_framework import permissions


class IsAuthorAuthenticatedOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        """Ограничения всего запроса"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Ограничения запроса к одному объекту"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
