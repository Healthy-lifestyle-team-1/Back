# Generated by Django 5.0.6 on 2024-05-29 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_app', '0005_alter_customer_allergies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dishhalf',
            name='calories',
            field=models.FloatField(default=0, max_length=10, verbose_name='Калории'),
        ),
        migrations.AlterField(
            model_name='dishhalf',
            name='carbs',
            field=models.FloatField(default=0, max_length=10, verbose_name='Углеводы'),
        ),
        migrations.AlterField(
            model_name='dishhalf',
            name='fats',
            field=models.FloatField(default=0, max_length=10, verbose_name='Жиры'),
        ),
        migrations.AlterField(
            model_name='dishhalf',
            name='proteins',
            field=models.FloatField(default=0, max_length=10, verbose_name='Протеины'),
        ),
    ]
