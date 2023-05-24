from Core.serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView as BaseTokenObtainPairView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
class TokenObtainPairView(BaseTokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

class RegisterUsersViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.none()
    serializer_class = RegisterSerializer