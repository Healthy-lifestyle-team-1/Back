from rest_framework import serializers
from .models import User


class UserLoginRegisterSerializer(serializers.Serializer):
    login = serializers.CharField()


class VerifyCodeSerializer(serializers.Serializer):
    login = serializers.CharField()
    code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone', 'username']
        
    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("This phone number is already in use.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value
