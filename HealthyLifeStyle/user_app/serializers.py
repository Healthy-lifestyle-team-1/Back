from rest_framework import serializers
from .models import User


class UserRegisterSerializer(serializers.Serializer):
    login = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    
    def validate_login(self, value):
        if '@' in value:
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("This email is already in use.")
        else:
            if not value.isdigit():
                raise serializers.ValidationError("Phone number must contain only digits.")
            if len(value) != 11:
                raise serializers.ValidationError("Phone number must be exactly 11 digits.")
            if User.objects.filter(phone=value).exists():
                raise serializers.ValidationError("This phone number is already in use.")
        return value


class UserLoginSerializer(serializers.Serializer):
    login = serializers.CharField(required=True)


class VerifyCodeSerializer(serializers.Serializer):
    login = serializers.CharField(required=True)
    code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone', 'username']
        
    def validate_phone(self, value):
        if len(value) != 11:
            raise serializers.ValidationError("Phone number must be exactly 11 digits.")
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("This phone number is already in use.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value
