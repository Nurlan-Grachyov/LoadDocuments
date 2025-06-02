from rest_framework.permissions import BasePermission


class Moderators(BasePermission):
    """
    Check for access rights.
    If the method is GET, PUT or PATCH, returns True if the user is superuser or belongs to the Moderators group.
    If the method is POST, returns True if the user is superuser or authenticated.
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user.is_superuser or (
                request.user.is_authenticated
                and not request.user.groups.filter(name="Moderators").exists()
            )
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "PUT", "PATCH"):
            return (
                request.user.groups.filter(name="Moderators").exists()
                or request.user.is_superuser
            )
        return False


class IsSuperUser(BasePermission):
    """
    Check for access rights.
    If the method is DELETE, returns True if the user is superuser.
    """

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return request.user.is_superuser
        return False
