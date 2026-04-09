from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsProvider(BasePermission):
    def has_permission(self, request, view):
        return(
            request.user.is_authenticated and
            request.user.user_type == 'P'
        )
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.provider == request.user