from Core.serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView as BaseTokenObtainPairView


class TokenObtainPairView(BaseTokenObtainPairView):
    serializer_class = TokenObtainPairSerializer