from rest_framework import serializers
from .models import *


# Сериализаторы для моделей
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'category', 'image', 'calories',
                  'proteins', 'fats', 'carbs', 'price', 'rating']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['product', 'user', 'value']


class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = ['name']


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['author', 'date_created', 'text']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name']


# class CombinationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Combination
#         fields = ['half1', 'half2']
