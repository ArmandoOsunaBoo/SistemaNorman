# Generated by Django 3.2.5 on 2021-11-24 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0008_auto_20211124_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Nombre'),
        ),
    ]
