# Generated by Django 5.0.6 on 2024-06-20 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_mark_is_approved_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userslevel',
            name='level',
            field=models.IntegerField(default=0, verbose_name='Уровень пользователя'),
        ),
        migrations.AlterField(
            model_name='userslevel',
            name='total_points',
            field=models.IntegerField(default=0, verbose_name='Очки пользователя'),
        ),
    ]