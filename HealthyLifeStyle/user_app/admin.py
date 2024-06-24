from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'phone', 'email', 'date_joined')
    search_fields = ('phone', 'email')
    list_filter = ('date_joined', 'is_staff', 'is_active')
    ordering = ('date_joined',)


# Регистрируем модели в админке
admin.site.register(User, UserAdmin)
