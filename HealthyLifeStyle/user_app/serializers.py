from rest_framework import serializers
from .models import User


class UserLoginSerializer(serializers.Serializer):
    login = serializers.CharField(required=True)
    username = serializers.CharField(required=False, allow_null=True)
    
    def validate_login(self, value):
        if '@' not in value:
            if not value.isdigit():
                raise serializers.ValidationError("Phone number must contain only digits.")
            if len(value) != 11:
                raise serializers.ValidationError("Phone number must be exactly 11 digits.")
        return value


class VerifyCodeSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'username']
        
    def validate_phone(self, value):
        user = self.instance
        if len(value) != 11:
            raise serializers.ValidationError("Phone number must be exactly 11 digits.")
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if User.objects.filter(phone=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("This phone number is already in use.")
        return value

    def validate_email(self, value):
        user = self.instance
        if User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value
