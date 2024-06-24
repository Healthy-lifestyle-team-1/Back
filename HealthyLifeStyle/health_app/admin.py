from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'price')
    search_fields = ('title',)
    list_filter = ('category', 'tag', 'price')


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author', 'date_created')
    search_fields = ('author',)
    list_filter = ('date_created',)


class NewsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author', 'date_created')
    search_fields = ('author',)
    list_filter = ('date_created',)


# Регистрируем модели в админке
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Rating)
admin.site.register(Cart)
admin.site.register(Tag)
admin.site.register(CartItem)
admin.site.register(Like)
# admin.site.register(Allergy)
# admin.site.register(Ingredient)
# admin.site.register(Combination)
