from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class RetrieveUpdateModelMixin(ModelViewSet):
    """Gives HTTP_405 for retrieve and patch methods."""

    def retrieve(self, request, *args, **kwargs):
        return Response(
            {'error': 'Метод не доступен'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(
            {'error': 'Метод не доступен'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED)
