# Generated by Django 4.2.4 on 2023-08-22 04:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0020_order_archived'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productorder',
            name='count',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]