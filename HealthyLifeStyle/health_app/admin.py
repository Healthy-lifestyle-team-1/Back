from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(DishHalf)
admin.site.register(Combination)
admin.site.register(Allergy)
