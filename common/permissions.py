from rest_framework.permissions import BasePermission

from accounts.models import User, UserRoles


class OnlyAdminPermission(BasePermission):

    def has_permission(self, request, view):
        user: User = request.user
        return user.is_included_in_any_group([UserRoles.super_admin.name, UserRoles.admin.name])