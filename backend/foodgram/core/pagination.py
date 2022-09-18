from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """Добавляет возможность изменять кол-во объектов на странице."""

    page_size_query_param = "limit"
    max_page_size = 100
