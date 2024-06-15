from rest_framework import serializers

from user_app.serializers import UserSerializer
from .models import *


# Сериализаторы для моделей
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


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


class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['cart', 'product', 'quantity', 'total_price']
        

    def get_total_price(self, obj):
        return obj.get_total_price()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, source='cartitem_set', read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['user', 'items', 'created_at', 'total_price']

    def get_total_price(self, obj):
        total = sum(item.get_total_price() for item in obj.cartitem_set.all())
        return total


# class IngredientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ingredient
#         fields = ['name']

# class CombinationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Combination
#         fields = ['half1', 'half2']
