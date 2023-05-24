from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet

class CustomModelViewSet(ListModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    # This class is used to create a custom viewset that has the list, retrieve and destroy actions
    pass

class NoDeleteModelViewSet(ListModelMixin,RetrieveModelMixin,UpdateModelMixin,CreateModelMixin,GenericViewSet):
    # This class is used to create a custom viewset that has the list, retrieve and update actions
    pass