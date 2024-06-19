from rest_framework import serializers

from user_app.serializers import UserSerializer
from .models import *


# Сериализаторы для моделей
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_rating(self, obj):
        return obj.average_rating()

    def get_likes(self, obj):
        return obj.like_amount()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'product', 'value']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context.get('user')
        if user:
            validated_data['user'] = user
        return super().create(validated_data)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'product']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context.get('user')
        if user:
            validated_data['user'] = user
        return super().create(validated_data)

    def validate(self, data):
        user = self.context.get('user')
        product = data['product']
        if Like.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("Вы уже лайкнули этот продукт.")
        return data


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'author', 'date_created', 'text']


class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    product = ProductSerializer()  # Включаем данные о продукте

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']
        read_only_fields = ['cart']

    # Общая стоимость позиции корзины
    def get_total_price(self, obj):
        return obj.get_total_price()

    # Добавление корзины в поле для создания позиции
    def create(self, validated_data):
        cart = self.context.get('cart')
        if cart:
            validated_data['cart'] = cart
        return super().create(validated_data)


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, source='cartitem_set', read_only=True)
    total_price = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at', 'total_price']

    # Общая стоимость корзины
    def get_total_price(self, obj):
        total = sum(item.get_total_price() for item in obj.cartitem_set.all())
        return total

    # Добавление пользователя в поле для создания корзины
    def create(self, validated_data):
        user = self.context.get('user')
        if user:
            validated_data['user'] = user
        return super().create(validated_data)

    def validate(self, data):
        user = self.context.get('user')
        if Cart.objects.filter(user=user).exists():
            raise serializers.ValidationError("У вас уже есть корзина.")
        return data

# class AllergySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Allergy
#         fields = ['name']

# class IngredientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ingredient
#         fields = ['name']

# class CombinationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Combination
#         fields = ['half1', 'half2']
