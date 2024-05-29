from django.db import models
from django.contrib.auth.models import User


# Данные пользователя
class Customer(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    #ACTIVITY_LEVEL_CHOICES = [
    #    (1.2, 'Минимальная активность, сидячая работа'),
    #    (1.375, 'Слабый уровень активности'),
    #    (1.55, 'Умеренный уровень активности'),
    #    (1.7, 'Тяжелая или трудоемкая активность'),
    #    (1.9, 'Экстремальный уровень активности'),
    #]

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Связь один-к-одному с моделью User
    name = models.CharField(max_length=10, verbose_name='Имя')
    fam = models.CharField(max_length=20, verbose_name='Фамилия')
    phone = models.TextField(max_length=15, null=True, verbose_name='Телефон')
    email = models.EmailField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Пол')
    weight = models.FloatField(max_length=3, verbose_name='Вес')
    height = models.FloatField(max_length=3, verbose_name='Рост')
    age = models.IntegerField(verbose_name='Возраст')
    allergies = models.TextField(blank=True, null=True, verbose_name='Список аллергенов')
    #activity_level = models.FloatField(choices=ACTIVITY_LEVEL_CHOICES, default=1.2, verbose_name='Уровень активности')

    # Алгоритм расчёта КБЖУ по методу Миффлина-Сан Жеора
    def calculate_kbju(self):
        if self.gender == 'M':
            bmr = (10 * self.weight + 6.25 * self.height - 5 * self.age + 5) * self.activity_level
        elif self.gender == 'F':
            bmr = (10 * self.weight + 6.25 * self.height - 5 * self.age - 161) * self.activity_level
        # Примерные пропорции для расчета КБЖУ
        proteins = bmr * 0.3 / 4
        fats = bmr * 0.25 / 9
        carbs = bmr * 0.45 / 4

        return {
            'calories': bmr,
            'proteins': proteins,
            'fats': fats,
            'carbs': carbs
        }


# Категории блюд
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Категория')

    def __str__(self):
        return self.name


# Половинки тарелок
class DishHalf(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, related_name='dish_halves', on_delete=models.CASCADE, null=True, blank=True)
    calories = models.FloatField(max_length=10, verbose_name='Калории')
    proteins = models.FloatField(max_length=10, verbose_name='Протеины')
    fats = models.FloatField(max_length=10, verbose_name='Жиры')
    carbs = models.FloatField(max_length=10, verbose_name='Углеводы')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.name


# Комбинации
class Combination(models.Model):
    half1 = models.ForeignKey(DishHalf, related_name='half1', on_delete=models.CASCADE, null=True)
    half2 = models.ForeignKey(DishHalf, related_name='half2', on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('half1', 'half2')

    def __str__(self):
        return self.half1.name + '-' + self.half2.name


# Аллергия
class Allergy(models.Model):
    name = models.CharField(max_length=255)
    dish_halves = models.ManyToManyField(DishHalf)



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
