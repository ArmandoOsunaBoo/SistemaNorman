# Generated by Django 3.2.5 on 2022-01-17 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0013_attendance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Incidences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=90, verbose_name='Numero empleado')),
                ('name', models.CharField(blank=True, max_length=20, verbose_name='Nombre')),
                ('incidence', models.CharField(blank=True, max_length=20, verbose_name='Incidencia')),
                ('date', models.CharField(blank=True, max_length=20, verbose_name='Fecha')),
                ('hours', models.CharField(blank=True, max_length=20, verbose_name='Hours')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Fecha Modificación')),
            ],
        ),
    ]
