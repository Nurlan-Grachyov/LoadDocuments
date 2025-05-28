from rest_framework.permissions import BasePermission


class Moderators(BasePermission):
    """
    Проверка на права доступа.
    Если метод GET, PUT или PATCH, вернет True, если пользователь superuser или входит в группу Moderators.
    Если метод POST, вернет True, если пользователь superuser или owner.
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user.is_superuser or request.user.is_authenticated and not request.user.groups.filter(name="Moderators").exists()
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ("GET",):
            return (
                    request.user.groups.filter(name="Moderators").exists()
                    or request.user.is_superuser or request.user == obj.owner
            )
        elif request.method in ("PUT", "PATCH"):
            return (
                    request.user.groups.filter(name="Moderators").exists()
                    or request.user.is_superuser
            )
        return False


class IsSuperUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return request.user.is_superuser
        return False
