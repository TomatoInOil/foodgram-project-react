from rest_framework import mixins
from rest_framework import viewsets


class ListRetrieveViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    Вьюсет обеспечивает `retrieve` и `list` действия.
    """

    pass
