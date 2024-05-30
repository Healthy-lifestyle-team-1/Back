from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DishHalfViewSet(viewsets.ModelViewSet):
    queryset = DishHalf.objects.all()
    serializer_class = DishHalfSerializer


class CombinationViewSet(viewsets.ModelViewSet):
    queryset = Combination.objects.all()
    serializer_class = CombinationSerializer


class AllergyViewSet(viewsets.ModelViewSet):
    queryset = Allergy.objects.all()
    serializer_class = AllergySerializer
