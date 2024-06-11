# Generated by Django 5.0.6 on 2024-06-11 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_app', '0003_product_cooking_method_product_weight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='ingredients',
        ),
        migrations.AlterField(
            model_name='product',
            name='is_prepared',
            field=models.BooleanField(verbose_name='Готово'),
        ),
        migrations.DeleteModel(
            name='Ingredient',
        ),
    ]