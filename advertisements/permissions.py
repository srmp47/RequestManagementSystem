from rest_framework import permissions

class IsOwnerOrSupport(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_support or request.user.is_superuser:
            return True
        return obj.user == request.user

class IsContractor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_contractor or request.user.is_superuser)