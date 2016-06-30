from rest_framework import permissions

# __author__ = 'Sourav Banerjee'
# __email__ = ' srvasn@gmail.com'
#

class IsStaffOrTargetUser(permissions.BasePermission):
    """
    Used to govern access for generic User ModelViewSet
    """
    def has_permission(self, request, view):
        return view.action == 'retrieve' or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Governs access to user created records. Staff users can view everything.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user.is_staff:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.creator == request.user
