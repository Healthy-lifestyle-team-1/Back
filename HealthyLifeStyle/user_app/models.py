from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone
from datetime import timedelta
import uuid


# Модель менеджера
class UserManager(BaseUserManager):
    def create_user(self, phone, email, password=None, **extra_fields):
        user = self.model(phone=phone, email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, email, password, **extra_fields)


# Данные пользователя
class User(AbstractUser, PermissionsMixin):

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    # GENDER_CHOICES = [
    #     ('M', 'Male'),
    #     ('F', 'Female'),
    # ]
    
    objects = UserManager()
    
    username = models.CharField(max_length=20, null=True, verbose_name='Имя')
    phone = models.CharField(max_length=15, null=True, unique=True, verbose_name='Телефон')
    email = models.EmailField(max_length=50, null=True, blank=True, unique=True)
    password = models.CharField(max_length=20, null=True, blank=True, verbose_name='Пароль')
    # gender = models.CharField(max_length=1, null=True, choices=GENDER_CHOICES, verbose_name='Пол')
    # weight = models.FloatField(max_length=3, null=True, verbose_name='Вес')
    # height = models.FloatField(max_length=3, null=True, verbose_name='Рост')
    # age = models.IntegerField(max_length=3, null=True, verbose_name='Возраст')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания аккаунта')
    verification_code = models.CharField(max_length=6, blank=True, null=True, verbose_name='Код верификации')
    code_expiry = models.DateTimeField(blank=True, null=True, verbose_name='Срок действия кода')
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username', 'email']
    
    def generate_verification_code(self):
        code = str(uuid.uuid4().int)[:6]
        self.verification_code = code
        self.code_expiry = timezone.now() + timedelta(minutes=5)
        self.save()
        return code
    
    def __str__(self):
        if self.phone:
            return f'{self.username}|{self.phone}'
        return f'{self.username}|{self.email}'
