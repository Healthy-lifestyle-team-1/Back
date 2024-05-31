from django.db import models
from user_app.models import User


# Категории блюд
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Категория')

    def __str__(self):
        return self.name


# Аллергия
class Allergy(models.Model):
    # Коровье молоко
    # Яйца
    # Арахис
    # Рыба
    # Моллюски
    # Древесные орехи, такие как кешью или грецкие орехи.
    # Пшеница
    # Соя
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name


# Половинки тарелок
class DishHalf(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название')
    category = models.ForeignKey(Category, related_name='dish_halves', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Категория')
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    # TODO Уточнить работу API с фото
    calories = models.FloatField(max_length=10, verbose_name='Калории')
    proteins = models.FloatField(max_length=10, verbose_name='Протеины')
    fats = models.FloatField(max_length=10, verbose_name='Жиры')
    carbs = models.FloatField(max_length=10, verbose_name='Углеводы')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена')
    contraindications = models.ManyToManyField(Allergy, blank=True, verbose_name='Противопоказания')
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True) # 4.11

    def __str__(self):
        return self.name


# Комбинации
class Combination(models.Model):
    half1 = models.ForeignKey(DishHalf, related_name='half1', on_delete=models.CASCADE,
                              null=True, verbose_name='Первая половина')
    half2 = models.ForeignKey(DishHalf, related_name='half2', on_delete=models.CASCADE,
                              null=True, verbose_name='Вторая половина')

    class Meta:
        unique_together = ('half1', 'half2')

    def __str__(self):
        return f'{self.half1} - {self.half2.name}'


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    text = models.TextField(verbose_name='Текст')

    def __str__(self):
        return f'{self.author}|{self.date_created}|{self.text[:20]}'


# =============== На доработке ===============
# class Cart(models.Model):
#     user = models.ForeignKey(Customer, related_name='carts', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)


# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
#     dish_half = models.ForeignKey(DishHalf, related_name='+', on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)


# class Order(models.Model):
#     user = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
#     dish_half = models.ForeignKey(DishHalf, related_name='+', on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     price = models.DecimalField(max_digits=6, decimal_places=2)
