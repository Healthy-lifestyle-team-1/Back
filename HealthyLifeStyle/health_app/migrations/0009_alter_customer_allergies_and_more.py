# Generated by Django 5.0.6 on 2024-05-29 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health_app', '0008_remove_allergy_dish_halves_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='allergies',
            field=models.ManyToManyField(blank=True, to='health_app.allergy', verbose_name='Список аллергенов'),
        ),
        migrations.AlterField(
            model_name='dishhalf',
            name='contraindications',
            field=models.ManyToManyField(blank=True, to='health_app.allergy'),
        ),
    ]
