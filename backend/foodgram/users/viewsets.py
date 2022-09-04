from rest_framework import mixins, viewsets


class ListRetrieveCreateViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """Вьюсет обеспечивает `list`, `retrieve` и `create` действия."""

    pass
