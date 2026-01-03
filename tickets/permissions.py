from rest_framework import permissions


class IsSupportOrSender(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_support or request.user.is_superuser:
            return True

        return obj.sender == request.user