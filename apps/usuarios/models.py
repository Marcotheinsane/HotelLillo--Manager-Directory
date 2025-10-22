from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# PERFIL de empleado para empleados del hotel admin y recepcionistas del hotel lillo
#

class Perfil_empleado(models.Model):
    ROLES= (
        ('administrador','Administrador'),
        ('recepcionista','Recepcionistas'),
    )

    perfil_empleado= models.OneToOneField(User,on_delete=models.CASCADE)
    nombre= models.CharField(max_length=40)
    rol= models.CharField(max_length=40,choices=ROLES)
    rut= models.CharField(max_length=12)

    def __str__(self):
        return f"{self.perfil_empleado} - {self.nombre} - {self.rol}"

# PERFIL de huesped con datos obligatorios
class Huesped(models.Model):
    TIPO_DOCUMENTO = (
        ('rut', 'RUT'),
        ('pasaporte', 'Pasaporte'),
    )# la razon de de usar plantillas es para que solo se puedan escoger solo 2 opciones con choice
    
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOCUMENTO)
    numero_documento = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    

    def __str__(self) -> str:
        return f"{self.nombre} {self.apellido}"