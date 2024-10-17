# Generated by Django 4.2 on 2024-10-13 20:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_remove_employeeteam_unique_employee_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeassesmentskill',
            name='assesment',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Оценка навыка сотрудника'),
        ),
        migrations.AlterField(
            model_name='employeeengagement',
            name='performance_score',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='Уровень вовлеченности сотрудника'),
        ),
    ]