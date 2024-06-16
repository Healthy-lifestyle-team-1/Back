from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Allergy)
admin.site.register(Article)
admin.site.register(Rating)
admin.site.register(Cart)
admin.site.register(Tag)
admin.site.register(CartItem)
# admin.site.register(Ingredient)
# admin.site.register(Combination)
