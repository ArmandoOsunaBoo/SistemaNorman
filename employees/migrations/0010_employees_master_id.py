# Generated by Django 3.2.5 on 2021-11-25 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0009_alter_employees_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='employees',
            name='master_id',
            field=models.CharField(blank=True, max_length=20, verbose_name='Master ID'),
        ),
    ]
