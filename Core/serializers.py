from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from djoser.serializers import UserSerializer as BaseUserSerializer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from django.db import transaction, IntegrityError
from djoser.conf import settings 
from Core.models import User
class TokenObtainPairSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh_token'] = str(refresh)
        data['access_token'] = str(refresh.access_token)
        return data

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','first_name', 'last_name', 'password', 'email','username', 'account_type']
class RegisterSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta): 
        fields = ['id','first_name', 'last_name', 'password', 'email']
    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            username = validated_data.get("email")
            username = username.split('@')[0]
            user = User.objects.create_user(username = username, **validated_data)
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username','first_name', 'last_name','email']
        read_only_fields = ['username','email', 'account_type']