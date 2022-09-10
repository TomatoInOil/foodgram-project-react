from rest_framework import status
from rest_framework.response import Response


def create_response_with_error_message(
    msg, status=status.HTTP_400_BAD_REQUEST
):
    """Возвращает объект Response с сообщением об ошибке."""
    return Response(
        data={"error": msg},
        status=status,
    )
