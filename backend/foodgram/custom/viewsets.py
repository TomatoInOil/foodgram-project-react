from rest_framework import mixins
from rest_framework import viewsets


class ListRetrieveViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """Набор представлений, обеспечивающий `retrieve` и `list` действия."""

    pass


class CreateDestroyViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """Набор представлений, обеспечивающий `create` и `destroy` действия."""

    pass
