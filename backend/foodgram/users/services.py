from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from services.services import create_response_with_error_message
from users.models import Subscription

User = get_user_model()


def get_error_response_if_validation_of_request_subscription_failed(
    request, **kwargs
):
    """Получить ответ с ошибкой, если проверка запроса подписки провалена."""
    current_user, selected_user = _get_current_user_and_selected_user(
        request, **kwargs
    )
    result = {
        "response": None,
        "current_user": current_user,
        "selected_user": selected_user,
        "subscription": None,
    }
    result["response"] = _check_for_match_between_current_and_selected_user(
        current_user, selected_user
    )
    if result["response"]:
        return result
    subscription = _get_sub(current_user, selected_user)
    result["response"] = _check_existence_of_subscription(
        request, subscription
    )
    if result["response"]:
        return result
    result["subscription"] = subscription
    return result


def _get_sub(current_user, selected_user):
    """Получить подписку текущего пользователя на выбранного."""
    return Subscription.objects.filter(
        author=selected_user, subscriber=current_user
    )


def _get_current_user_and_selected_user(request, **kwargs):
    """Получить из запроса текущего пользователя и выбранного автора."""
    current_user = request.user
    author = get_object_or_404(User, pk=kwargs.get("author_id", None))
    return current_user, author


def _check_for_match_between_current_and_selected_user(
    current_user, selected_user
):
    """Проверяет на совпадение текущего и выбранного пользователей."""
    if current_user == selected_user:
        return create_response_with_error_message(
            msg="Текущий пользователь и выбранный совпадают."
        )
    return None


def _check_existence_of_subscription(request, subscription):
    """Проверяет наличие или отсуствие подписки."""
    delete = request.method == "DELETE"
    if delete and not subscription.exists():
        return create_response_with_error_message(msg="Подписка не оформлена.")
    if not delete and subscription.exists():
        return create_response_with_error_message(
            msg="Подписка уже оформлена."
        )
    return None
