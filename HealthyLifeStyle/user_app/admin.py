from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    # список или кортеж со всеми полями, отображаемыми в таблице с постами
    list_display = ('__str__', 'phone', 'email', 'date_joined')
    list_filter = ('date_joined', 'is_staff', 'is_active')  # фильтры по полям


# Регистрирую модели в админке
admin.site.register(User, UserAdmin)
