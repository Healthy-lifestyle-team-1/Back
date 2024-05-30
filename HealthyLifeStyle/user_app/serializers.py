from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from .models import User

UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('phone', 'email', 'password')

    def create(self, validated_data):
        phone = validated_data.get('phone')
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = UserModel.objects.create_user(email=email, phone=phone, password=password)
        user.save()
        return user



class UserLoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        login = data.get('login')
        password = data.get('password')

        if '@' in login:
            # Это выглядит как email
            user = User.objects.filter(email=login).first()
        else:
            # Иначе, это, вероятно, телефон
            user = User.objects.filter(phone=login).first()

        if user and user.check_password(password):
            backend = 'django.contrib.auth.backends.ModelBackend'
            data['user'] = user
            data['backend'] = backend
            return data

        raise ValidationError('User not found or invalid credentials')

    def check_user(self, validated_data):
        return validated_data.get('user'), validated_data.get('backend')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('email', 'phone', 'username', 'fam')
