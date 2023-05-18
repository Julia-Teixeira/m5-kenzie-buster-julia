from rest_framework import permissions
from rest_framework.views import Request, View
from .models import User


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_superuser
        )


class IsAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: User):
        if request.user.is_employee:
            return True
        else:
            return obj == request.user
