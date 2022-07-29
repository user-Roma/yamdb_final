from rest_framework import permissions

from reviews.models import User


class AdminOrReadOnly(permissions.BasePermission):
    """Access for non safety methods only for Admin."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        return request.user.role in (User.ADMIN,)


class AuthorAdminModerOrReadOnly(permissions.BasePermission):
    """
    Access to create only for authenticated users,
    to patch, delete for author, admin, moderator,
    or read only.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        return obj.author == request.user or (
            request.user.role in (User.ADMIN, User.MODERATOR))


class AdminOnly(permissions.BasePermission):
    """Access for non all methods only for Admin."""

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.role in (User.ADMIN,) or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.role in (User.ADMIN,) or request.user.is_superuser
