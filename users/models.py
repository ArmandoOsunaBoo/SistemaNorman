from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile_user")

    AREA_LIST = (
        ('Recursos Humanos', 'Recursos Humanos'),
        ('Finanzas', 'Finanzas'),
        ('Admin', 'Admin'),
        ('Gerencia', 'Gerencia'),
        ('Comun', 'Comun'),
    )
    area = models.CharField(max_length=20,blank=True,choices=AREA_LIST)
    TYPE_LIST = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    )
    type = models.CharField(max_length=20,blank=True,choices=TYPE_LIST)
    active = models.CharField(max_length=20,blank=True,default="Activo")
    picture = models.ImageField(upload_to='users/pictures',blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username