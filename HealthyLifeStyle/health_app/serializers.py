from rest_framework import serializers
from .models import *


# Сериализаторы для моделей
class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = '__all__'
    
    # Метод для создания нового объекта
    def create(self, validated_data):
        client = Customer.objects.create(**validated_data)
        return client


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class DishHalfSerializer(serializers.ModelSerializer):
    class Meta:
        model = DishHalf
        fields = ['name', 'category', 'image', 'calories',
                  'proteins', 'fats', 'carbs', 'price', 'rating']


class CombinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Combination
        fields = ['half1', 'half2']


class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = ['name']
