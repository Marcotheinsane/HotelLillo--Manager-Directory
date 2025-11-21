from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .validators import validar_rut, validar_telefono

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

    def clean(self):
        errors = {}
        if self.nombre and len(self.nombre.strip()) < 2:
            errors['nombre'] = 'El nombre es muy corto.'
        if self.rut:
            try:
                validar_rut(self.rut)
            except ValidationError as e:
                errors['rut'] = e.messages
        if errors:
            raise ValidationError(errors)


class Huesped(models.Model):
    TIPO_DOCUMENTO = (
        ('rut', 'RUT'),
        ('pasaporte', 'Pasaporte'),
    )
    
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOCUMENTO)
    numero_documento = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    

    def __str__(self) -> str:
        return f"{self.nombre} {self.apellido}"

    def clean(self):
        errors = {}
        if self.nombre and len(self.nombre.strip()) < 2:
            errors['nombre'] = 'El nombre es muy corto.'
        if self.apellido and len(self.apellido.strip()) < 2:
            errors['apellido'] = 'El apellido es muy corto.'
        if self.tipo_documento == 'rut' and self.numero_documento:
            try:
                validar_rut(self.numero_documento)
            except ValidationError as e:
                errors['numero_documento'] = e.messages
        if self.telefono:
            try:
                validar_telefono(self.telefono)
            except ValidationError as e:
                errors['telefono'] = e.messages
        if errors:
            raise ValidationError(errors)