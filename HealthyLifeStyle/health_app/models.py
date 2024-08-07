from django.db import models
from django.core.exceptions import ValidationError
from user_app.models import User
from django_ckeditor_5.fields import CKEditor5Field


# Категория
class Category(models.Model):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name


# Тег
class Tag(models.Model):

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name


# Продукт
class Product(models.Model):

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    TYPES_OF_PREPARING = [
        ('PR', 'Готовое блюдо'),
        ('H1', 'Первая половинка'),
        ('H2', 'Вторая половинка'),
    ]

    title = models.CharField(max_length=255, unique=True, verbose_name='Название')
    subtitle = models.CharField(max_length=255, default='', verbose_name='Развернутое название')
    category = models.ManyToManyField(Category, blank=True, verbose_name='Категория')
    tag = models.ManyToManyField(Tag, blank=True, verbose_name='Тэг')
    image = models.ImageField(upload_to='images/', verbose_name='Фотография', null=True, blank=True)  # Можно поставить default
    image_extra = models.ImageField(upload_to='images/', verbose_name='Фотография половинки', null=True, blank=True)
    calories = models.FloatField(max_length=10, verbose_name='Калории')
    proteins = models.FloatField(max_length=10, verbose_name='Протеины')
    fats = models.FloatField(max_length=10, verbose_name='Жиры')
    carbs = models.FloatField(max_length=10, verbose_name='Углеводы')
    # price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена')
    price = models.PositiveIntegerField(verbose_name='Цена')
    description = models.TextField(default='', verbose_name='Описание')
    cooking_method = models.TextField(default="", null=True, verbose_name='Метод приготовления')
    weight = models.IntegerField(default=0, null=True, verbose_name='Вес')
    ingredients = models.TextField(blank=True, verbose_name='Продукты')
    is_prepared = models.CharField(max_length=2, default='PR', choices=TYPES_OF_PREPARING, verbose_name='Тип продукта')

    # Высчитывание среднего рейтинга
    def average_rating(self):
        rating = self.rating.all()
        if rating:
            return sum(rate.value for rate in rating) / len(rating)
        return 0

    # Высчитывание лайков
    def like_amount(self):
        return self.likes.count()

    def __str__(self):
        return self.title


# Рейтинг
class Rating(models.Model):
    product = models.ForeignKey(Product, related_name='rating', on_delete=models.CASCADE, verbose_name='Продукт')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    value = models.IntegerField(verbose_name='Оценка')
    text = models.TextField(verbose_name='Текст', default='')

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return f'{self.user.username}|{self.product}|{self.value}'


# Лайк
class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, related_name='likes', on_delete=models.CASCADE, verbose_name='Продукт')

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user.username}|{self.product}'


# Статья
class Article(models.Model):

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    text = CKEditor5Field('Text', config_name='extends')

    def __str__(self):
        return f'{self.author}|{self.text[:20]}'


# Новости
class News(models.Model):

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    text = CKEditor5Field('Text', config_name='extends')

    def __str__(self):
        return f'{self.author}|{self.text[:20]}'


# Менеджер для модели Корзины
class CartManager(models.Manager):
    # Переписывание метода создания для ограничения по количеству
    def create(self, *args, **kwargs):
        if self.model.objects.filter(user=kwargs['user']).count() > 0:
            raise ValidationError('Достигнут лимит на создание обьектов')
        return super().create(*args, **kwargs)


# Корзина
class Cart(models.Model):

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    objects = CartManager()

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return f'Cart of {self.user.username}'


# Позиции корзины
class CartItem(models.Model):

    class Meta:
        verbose_name = 'Предмет корзины'
        verbose_name_plural = 'Предметы корзины'

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f'{self.quantity} of {self.product.title}'

    # Высчитывание всей суммы позиции
    def get_total_price(self):
        return self.product.price * self.quantity


# class Ingredient(models.Model):
#     class Meta:
#         verbose_name = 'Ингредиент'
#         verbose_name_plural = 'Ингредиенты'
#
#     name = models.CharField(max_length=255, verbose_name='Название')
#
#     def __str__(self):
#         return self.name

# # Комбинации
# class Combination(models.Model):
#     half1 = models.ForeignKey(DishHalf, related_name='half1', on_delete=models.CASCADE,
#                               null=True, verbose_name='Первая половина')
#     half2 = models.ForeignKey(DishHalf, related_name='half2', on_delete=models.CASCADE,
#                               null=True, verbose_name='Вторая половина', blank=True)
#
#     class Meta:
#         verbose_name = 'Комбинация'
#         verbose_name_plural = 'Комбинации'
#         unique_together = ('half1', 'half2')
#
#     def get_price(self):
#         if self.half2:
#             return self.half1.price + self.half2.price
#         return self.half1.price
#
#     def __str__(self):
#         if self.half2:
#             return f'{self.half1.name} - {self.half2.name}'
#         else:
#             return self.half1.name


# Аллергия
# class Allergy(models.Model):
#     # Коровье молоко
#     # Яйца
#     # Арахис
#     # Рыба
#     # Моллюски
#     # Древесные орехи, такие как кешью или грецкие орехи.
#     # Пшеница
#     # Соя
#
#     class Meta:
#         verbose_name = 'Аллергия'
#         verbose_name_plural = 'Аллергии'
#
#     name = models.CharField(max_length=255, verbose_name='Название')
#
#     def __str__(self):
#         return self.name
