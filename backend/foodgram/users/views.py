from django.contrib.auth import get_user_model

from users.serializers import UserSerializer
from custom.viewsets import ListRetrieveViewSet

User = get_user_model()


class UsersViewSet(ListRetrieveViewSet):
    """Представление для модели пользователей.
    Обеспечивает получение списка пользователей и информации об одном.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
