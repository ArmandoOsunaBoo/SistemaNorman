# Generated by Django 3.2.5 on 2021-12-29 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grocery_shop', '0008_order_shop_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='shop_name',
        ),
    ]