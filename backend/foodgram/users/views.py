from rest_framework import views, status
from rest_framework.response import Response

from users.services import (
    get_error_response_if_validation_of_request_subscription_failed,
)
from users.models import Subscription


class SubscribeView(views.APIView):
    """Представление для подписки/отписки на авторов."""

    def post(self, request, *args, **kwargs):
        """Подписывает текущего пользователя на автора."""
        result = (
            get_error_response_if_validation_of_request_subscription_failed(
                request, **kwargs
            )
        )
        if result["response"]:
            return result["response"]
        Subscription.objects.create(
            author=result["selected_user"], subscriber=result["current_user"]
        )
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        """Отписывает текущего пользователя от автора."""
        result = (
            get_error_response_if_validation_of_request_subscription_failed(
                request, **kwargs
            )
        )
        if result["response"]:
            return result["response"]
        result["subscription"].delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
