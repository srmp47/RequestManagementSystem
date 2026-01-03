from rest_framework import permissions


class DynamicPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        required_perm = getattr(view, 'required_permission', None)
        if required_perm:
            return request.user.has_perm(f'users.{required_perm}')

        return True