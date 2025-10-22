from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    """
    Modelo de usuario simple para el Hotel Lillo
    """
    ROLES = [
        ('admin', 'Administrador'),
        ('recepcionista', 'Recepcionista'),
    ]
    
    rol = models.CharField(max_length=20, choices=ROLES, default='recepcionista')
    telefono = models.CharField(max_length=15, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_rol_display()})"