from rest_framework import permissions


class OnlyAuthorsUpdateDelete(permissions.BasePermission):
    """Разрешения, позволяющие редактировать, удалять объект только авторам.
    Чтение разрешено всем пользователям."""

    message = "Только авторы могут редактировать и удалять рецепты."

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
