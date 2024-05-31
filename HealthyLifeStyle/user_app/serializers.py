from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserLoginRegisterSerializer(serializers.Serializer):
    login = serializers.CharField()


class VerifyCodeSerializer(serializers.Serializer):
    login = serializers.CharField()
    code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('email', 'phone', 'username')
