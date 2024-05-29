from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DishHalfViewSet(viewsets.ModelViewSet):
    queryset = DishHalf.objects.all()
    serializer_class = DishHalfSerializer


class CombinationViewSet(viewsets.ModelViewSet):
    queryset = Combination.objects.all()
    serializer_class = CombinationSerializer
