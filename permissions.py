# apps/wire/permissions.py
from rest_framework.permissions import BasePermission
from apps.users.models import QcUserModel


# -----------------------------------------------------
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return request.user and request.user.is_authenticated

        return (
            request.user
            and request.user.is_authenticated
            and (request.user.is_staff or request.user.groups.filter(name="Admin").exists())
        )


class IsManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        return request.user.groups.filter(name__in=["Manager", "Admin"]).exists()


class IsOperator(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        return request.user.groups.filter(name="Operator").exists()
