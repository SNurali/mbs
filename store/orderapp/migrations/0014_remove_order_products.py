# Generated by Django 4.2.4 on 2023-08-16 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0013_rename_product_productorder_productid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
    ]