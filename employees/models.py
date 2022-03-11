from django.db import models
import datetime
from django.contrib.auth.models import User
# Create your models here.


class Attendance(models.Model):
    date = models.CharField(max_length=20,blank=True,verbose_name='Fecha')
    time = models.CharField(max_length=20,blank=True,verbose_name='Hora')
    number = models.CharField(max_length=90,blank=True,verbose_name='Numero empleado')
    event = models.CharField(max_length=20,blank=True,verbose_name='Evento')
    device = models.CharField(max_length=60,blank=True,verbose_name='Checador')
    employee = models.CharField(max_length=60,blank=True,verbose_name='Master ID')
    
    created = models.DateTimeField(auto_now_add=True,verbose_name='Fecha Creación')
    modified = models.DateTimeField(auto_now=True,verbose_name='Fecha Modificación')

class Incidences(models.Model):
    number = models.CharField(max_length=90,blank=True,verbose_name='Numero empleado')
    name = models.CharField(max_length=20,blank=True,verbose_name='Nombre')
    incidence = models.CharField(max_length=20,blank=True,verbose_name='Incidencia')
    date = models.CharField(max_length=20,blank=True,verbose_name='Fecha')
    hours = models.CharField(max_length=20,blank=True,verbose_name='Hours')
    minutes=models.CharField(max_length=20,blank=True,verbose_name='Hours')
    day=models.CharField(max_length=20,blank=True,verbose_name='Day')
    created = models.DateTimeField(auto_now_add=True,verbose_name='Fecha Creación')
    modified = models.DateTimeField(auto_now=True,verbose_name='Fecha Modificación')

class Employees(models.Model):
    master_id = models.CharField(max_length=20,blank=True,verbose_name='Master ID')
    old_number = models.CharField(max_length=20,blank=True,verbose_name='Numero Antiguo')
    number = models.CharField(max_length=20,blank=True,verbose_name='Numero')
    name = models.CharField(max_length=100,blank=True,verbose_name='Nombre')
    group = models.CharField(max_length=30,blank=True,verbose_name='Grupo')
    team = models.CharField(max_length=30,blank=True,verbose_name='Equipo')
    personal = models.CharField(max_length=25,blank=True,verbose_name='Personal')
    department_rp = models.CharField(max_length=30,blank=True,verbose_name='Departamento RP')
    area_rp = models.CharField(max_length=100,blank=True,verbose_name='Area RP')
    position_rp = models.CharField(max_length=30,blank=True,verbose_name='Puesto RP')
    payroll = models.CharField(max_length=20,blank=True,verbose_name='Nómina')
    admission_date = models.CharField(max_length=20,blank=True,verbose_name='ALTA')
    antiquity= models.CharField(max_length=30,blank=True,verbose_name='Antiguedad')
    status= models.CharField(max_length=20,blank=True,verbose_name='Estatus')
    leaving_date = models.CharField(max_length=20,blank=True,verbose_name='Fecha de Baja')
    reason_of_leaving = models.CharField(max_length=50,blank=True,verbose_name='Causa de Baja')
    curp = models.CharField(max_length=40,blank=True,verbose_name='CURP')
    rfc = models.CharField(max_length=30,blank=True,verbose_name='RFC')
    nss = models.CharField(max_length=30,blank=True,verbose_name='NSS')
    birth_date = models.CharField(max_length=20,blank=True,verbose_name='Fecha de Nacimiento')
    age = models.CharField(max_length=20,blank=True,verbose_name='Edad')
    gender = models.CharField(max_length=20,blank=True,verbose_name='Sexo')
    department = models.CharField(max_length=30,blank=True,verbose_name='Departamento')
    position = models.CharField(max_length=100,blank=True,verbose_name='Puesto')
    jacket = models.CharField(max_length=60,blank=True,verbose_name='Chaleco')
    aplication = models.CharField(max_length=30,blank=True,verbose_name='Aplicación')
    performance = models.CharField(max_length=30,blank=True,verbose_name='Rendimiento')
    nationality = models.CharField(max_length=30,blank=True,verbose_name='Nacionalidad')
    place_of_birth = models.CharField(max_length=50,blank=True,verbose_name='Lugar de nacimiento')
    municipality = models.CharField(max_length=50,blank=True,verbose_name='Municipio')
    location = models.CharField(max_length=50,blank=True,verbose_name='Localidad')
    division = models.CharField(max_length=50,blank=True,verbose_name='Fraccionamiento')
    suburb = models.CharField(max_length=130,blank=True,verbose_name='Colonia')
    street = models.CharField(max_length=50,blank=True,verbose_name='Calle')
    house_number = models.CharField(max_length=20,blank=True,verbose_name='Número de Casa')
    studies = models.CharField(max_length=50,blank=True,verbose_name='Estudios')
    email = models.CharField(max_length=60,blank=True,verbose_name='Correo')
    phone = models.CharField(max_length=30,blank=True,verbose_name='Télefono')
    blood_type = models.CharField(max_length=40,blank=True,verbose_name='Tipo de Sangre')
    allergies = models.CharField(max_length=60,blank=True,verbose_name='Alergias')
    marital_status = models.CharField(max_length=30,blank=True,verbose_name='Estado Civil')
    route = models.CharField(max_length=40,blank=True,verbose_name='Ruta')
    bus_stop = models.CharField(max_length=40,blank=True,verbose_name='Parada')
    emergency_phone_1 = models.CharField(max_length=35,blank=True,verbose_name='Télefono de Emergencia 1')
    emergency_phone_2 = models.CharField(max_length=35,blank=True,verbose_name='Télefono de Emergencia 2')
    emergency_phone_3 = models.CharField(max_length=35,blank=True,verbose_name='Télefono de Emergencia 3')
    schedule = models.CharField(max_length=25,blank=True,verbose_name='Horario')
    number_of_children = models.CharField(max_length=100,blank=True,verbose_name='Número de Hijos')
    age_of_kid_1 = models.CharField(max_length=100,blank=True,verbose_name='Edad del hijo 1')
    age_of_kid_2 = models.CharField(max_length=100,blank=True,verbose_name='Edad del hijo 2')
    age_of_kid_3 = models.CharField(max_length=100,blank=True,verbose_name='Edad del hijo 3')
    age_of_kid_4 = models.CharField(max_length=100,blank=True,verbose_name='Edad del hijo 4')
    age_of_kid_5 = models.CharField(max_length=100,blank=True,verbose_name='Edad del hijo 5')
    id_noi = models.CharField(max_length=20,blank=True,verbose_name='ID NOI')
    boss_support = models.CharField(max_length=20,blank=True,verbose_name='Apoyo Jefe')
    relation = models.CharField(max_length=30,blank=True,verbose_name='Relación')
    
    picture = models.ImageField(upload_to='users/pictures',blank=True,null=True,verbose_name='Foto')
    created = models.DateTimeField(auto_now_add=True,verbose_name='Fecha Creación')
    modified = models.DateTimeField(auto_now=True,verbose_name='Fecha Modificación')

    @property
    def age(self):
        a=self.birth_date[0:10]
        """ 
        print(a[0:4])
        print(a[5:7])
        print(a[8:10])
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$") 
        """
        da=(datetime.date.today() - datetime.date(int(a[0:4]), int(a[5:7]), int(a[8:10]))   ).days
        a = ( int(da / 365.25))
        return a

    @property
    def antiquity_time(self):
        a=self.admission_date[0:10]
        print(self.name)
        print(a)
        da=(datetime.date.today() - datetime.date(int(a[0:4]), int(a[5:7]), int(a[8:10]))).days
        a = ( (da / 31.4))
        return "{:.2f}".format(a)

    def __str__(self):
        return self.name
        