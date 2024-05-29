from rest_framework import serializers
from .models import *


# Сериализатор для модели Client
class ClientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = '__all__'
    
    # Метод для создания нового объекта
    def create(self, validated_data):
        client = Customer.objects.create(**validated_data)
        return client


