# Generated by Django 3.2.5 on 2021-12-09 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grocery_shop', '0002_product_id_master'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='no_producto',
        ),
        migrations.AlterField(
            model_name='product',
            name='id_master',
            field=models.CharField(max_length=100, null=True, verbose_name='id_master'),
        ),
    ]
