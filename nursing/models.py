from django.db import models

# Create your models here.
class Consultas(models.Model):
    num = models.CharField(max_length=10,verbose_name="Número")
    #name = models.CharField(max_length=100,verbose_name="Nombre")
    #area = models.CharField(max_length=50,verbose_name="Causa")
    llave = models.CharField(max_length=15,verbose_name="llave",default="0")
    cause = models.CharField(max_length=300,verbose_name="Causa")
    diagnosis = models.CharField(max_length=200,verbose_name="Diagnostico")
    therapy = models.CharField(max_length=200,verbose_name="Tratamiento")
    doctor = models.CharField(max_length=100,verbose_name="Doctor")
    note = models.CharField(max_length=500,verbose_name="Nota")
    extra = models.CharField(max_length=100,verbose_name="Extra")
    created = models.DateTimeField(auto_now_add=True,verbose_name="Fecha de Creación")
    updated = models.DateTimeField(auto_now=True,verbose_name="Fecha de Actualización")

    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"

    def __self__(self):
        return self.name

class Diccionario(models.Model):
    cause = models.CharField(max_length=300,verbose_name="Causa", unique=True)
    diagnosis = models.CharField(max_length=200,verbose_name="Diagnostico")
    therapy = models.CharField(max_length=200,verbose_name="Terapia")

    class Meta:
        verbose_name = "Diccionario"
        verbose_name_plural = "Diccionario"

    def __self__(self):
        return self.name

class Diagnosticos(models.Model):
    llave = models.CharField(max_length=15,unique=True,verbose_name="llave",default="0")
    nombre = models.CharField(max_length=300,verbose_name="Nombre")

    class Meta:
        verbose_name = "Diagnostico"
        verbose_name_plural = "Diagnosticos"

    def __self__(self):
        return self.name