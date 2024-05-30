from rest_framework import serializers
from .models import *


# Сериализаторы для моделей
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
