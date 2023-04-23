from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet

class CustomModelViewSet(ListModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    # This class is used to create a custom viewset that has the list, retrieve and destroy actions
    pass