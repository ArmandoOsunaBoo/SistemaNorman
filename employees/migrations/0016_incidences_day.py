# Generated by Django 3.2.5 on 2022-01-28 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0015_incidences_minutes'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidences',
            name='day',
            field=models.CharField(blank=True, max_length=20, verbose_name='Day'),
        ),
    ]