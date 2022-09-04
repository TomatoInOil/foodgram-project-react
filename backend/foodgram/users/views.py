from django.contrib.auth import get_user_model

from users.serializers import UserSerializer
from users.viewsets import ListRetrieveCreateViewSet

User = get_user_model()


class UsersViewSet(ListRetrieveCreateViewSet):
    """Представление для модели пользователей.
    Обеспечивает получение списка пользователей, регистрацию и
    просмотр профиля пользователя.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
