# Generated by Django 3.2.5 on 2021-11-23 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='nivel',
            new_name='type',
        ),
    ]
