# Generated by Django 5.0.4 on 2024-05-09 06:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0005_alter_cartitems_cart_productimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='featured_product',
        ),
        migrations.RemoveField(
            model_name='category',
            name='icon',
        ),
    ]