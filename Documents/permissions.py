from rest_framework.permissions import BasePermission


class Moderators(BasePermission):
    """
    Проверка на права доступа.
    Если метод GET, PUT или PATCH, вернет True, если пользователь superuser или входит в группу Moderators.
    Если метод POST, вернет True, если пользователь superuser или owner.
    """

    def has_permission(self, request, view):
        if request.method in ("GET", "PUT", "PATCH"):
            return (
                    request.user.groups.filter(name="Moderators").exists()
                    or request.user.is_superuser
            )
        elif request.method == "POST":
            return request.user.is_superuser or request.user.owner
        return False