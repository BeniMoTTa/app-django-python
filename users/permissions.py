from rest_framework import permissions




class IsEmployeeOrNormalUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.is_superuser or obj == request.user:
            return True
        