from rest_framework import mixins, viewsets


class ListRetrieveViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """Набор представлений, обеспечивающий `retrieve` и `list` действия."""

    pass
