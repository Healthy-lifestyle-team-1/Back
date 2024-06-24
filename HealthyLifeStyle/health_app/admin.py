from django.contrib import admin
from .models import *

class ProductAdmin(admin.ModelAdmin):
    # список или кортеж со всеми полями, отображаемыми в таблице с постами
    list_display = ('__str__', 'price')
    list_filter = ('category', 'tag', 'price')  # фильтры по полям

# Register your models here.
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Article)
admin.site.register(Rating)
admin.site.register(Cart)
admin.site.register(Tag)
admin.site.register(CartItem)
admin.site.register(Like)
# admin.site.register(Allergy)
# admin.site.register(Ingredient)
# admin.site.register(Combination)
