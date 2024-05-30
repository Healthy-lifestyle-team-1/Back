from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


# Менеджер
class UserManager(BaseUserManager):
    def create_user(self, email=None, phone=None, password=None):
        if not email and not phone:
            raise ValueError('Необходимо ввести номер телефона или email')
        if not password:
            raise ValueError('Необходимо ввести пароль')

        email = self.normalize_email(email) if email else None
        user = self.model(email=email, phone=phone)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email=None, phone=None, password=None):
        user = self.create_user(email=email, phone=phone, password=password)
        user.is_superuser = True
        user.save()
        return user


# Данные пользователя
class User(AbstractBaseUser, PermissionsMixin):
    # GENDER_CHOICES = [
    #     ('M', 'Male'),
    #     ('F', 'Female'),
    # ]

    username = models.CharField(max_length=10, null=True, verbose_name='Имя')
    fam = models.CharField(max_length=20, null=True, verbose_name='Фамилия')
    phone = models.CharField(max_length=15, null=True, unique=True, verbose_name='Телефон')
    email = models.EmailField(max_length=50, unique=True, null=True, blank=True)
    # gender = models.CharField(max_length=1, null=True, choices=GENDER_CHOICES, verbose_name='Пол')
    # weight = models.FloatField(max_length=3, null=True, verbose_name='Вес')
    # height = models.FloatField(max_length=3, null=True, verbose_name='Рост')
    # age = models.IntegerField(max_length=3, null=True, verbose_name='Возраст')
    # allergies = models.TextField(blank=True, null=True, verbose_name='Список аллергенов')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания аккаунта')
    
    is_verified = models.BooleanField(default=False, verbose_name='verified')

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return f'{self.username} {self.fam}'
    
    def save(self, *args, **kwargs):
        if not self.email and not self.phone:
            raise ValueError('Необходимо ввести номер телефона или email')
        super().save(*args, **kwargs)