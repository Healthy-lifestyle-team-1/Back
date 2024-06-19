import django_filters
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, generics, permissions
from rest_framework import status
from rest_framework.response import Response
from .filters import ProductFilter
from .permissions import IsCartOwner, IsCartItemOwner
from .serializers import *
from .models import *


# Дженерики создания
class CategoryViewSet(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = 'name'

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()


class TagViewSet(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = 'name'

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()


class ProductViewSet(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()


class RatingViewSet(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product', 'value']
    search_fields = ['product', 'value']
    ordering_fields = ['product', 'value']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'user': self.request.user
        })
        return context

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)


class LikeViewSet(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product']
    search_fields = ['product']
    ordering_fields = ['product']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'user': self.request.user
        })
        return context

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)


class ArticleViewSet(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'date_created']
    search_fields = ['author', 'date_created']
    ordering_fields = ['author', 'date_created']
    ordering = '-date_created'

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()


class CartViewSet(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        print(f"Cart of {self.request.user}")  # Отладочная информация
        return Cart.objects.filter(user=self.request.user)


class CartItemViewSet(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsCartItemOwner, permissions.IsAuthenticated]

    # Сохраняет корзину пользователя
    def get_serializer_context(self):
        context = super().get_serializer_context()
        cart = Cart.objects.get(user=self.request.user)
        context.update({
            'cart': cart,
        })
        return context

    # Выдаются только позиции пользователя
    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)


class CategoryUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class ProductUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]


class ArticleUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAdminUser]


class CartItemUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsCartItemOwner]


# class CartUpdateView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer
#     permission_classes = [IsCartOwner]
#
#     def get_queryset(self):
#         print(Cart.objects.filter(user=self.request.user))
#         return Cart.objects.filter(user=self.request.user)

# class AllergyUpdateView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Allergy.objects.all()
#     serializer_class = AllergySerializer
#     permission_classes = [permissions.IsAdminUser]

# class IngredientViewSet(generics.ListCreateAPIView):
#     queryset = Ingredient.objects.all()
#     serializer_class = IngredientSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['name']
#     search_fields = ['name']
#     ordering_fields = ['name']
#     ordering = ['name']
#
#     def get_permissions(self):
#         if self.request.method == 'GET':
#             self.permission_classes = [permissions.AllowAny]
#         else:
#             self.permission_classes = [permissions.IsAdminUser]
#         return super().get_permissions()

# class CombinationViewSet(generics.ListCreateAPIView):
#     queryset = Combination.objects.all()
#     serializer_class = CombinationSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['half1', 'half2']
#     search_fields = ['half1', 'half2']
#     ordering_fields = ['half1', 'half2']
#
#     def get_permissions(self):
#         if self.request.method == 'GET':
#             self.permission_classes = [permissions.AllowAny]
#         else:
#             self.permission_classes = [permissions.IsAdminUser]
#         return super().get_permissions()

# class AllergyViewSet(generics.ListCreateAPIView):
#     queryset = Allergy.objects.all()
#     serializer_class = AllergySerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['name']
#     search_fields = ['name']
#     ordering_fields = ['name']
#     ordering = 'name'
#
#     def get_permissions(self):
#         if self.request.method == 'GET':
#             self.permission_classes = [permissions.AllowAny]
#         else:
#             self.permission_classes = [permissions.IsAdminUser]
#         return super().get_permissions()
