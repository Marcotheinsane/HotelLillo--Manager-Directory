from django.db import models

#modulos externos
from apps.usuarios.models import Huesped
from apps.habitaciones.models import Habitacion


class RegistroReservas(models.Model):
    ESTADO_CHOICES = [
        ("pendiente", "Pendiente"),
        ("confirmada", "Confirmada"), 
        ("cancelada", "Cancelada")
    ]
    
    fecha_check_in = models.DateField(
        help_text="Ingrese Fecha de entrada"
    )
    fecha_check_out = models.DateField(
        help_text="Ingrese Fecha de salida"
    )
    estado_reserva = models.CharField(
        choices=ESTADO_CHOICES,
        default="pendiente",
        max_length=15 
    )
    Huespedes =  models.ForeignKey(
        Huesped,
        on_delete=models.CASCADE
    )
    Habitaciones = models.ForeignKey(
        Habitacion,
        on_delete=models.CASCADE
    )
    Estado_Habitacion =models.CharField(
        choices=Habitacion.ESTADO_CHOICES,
        max_length=15,
    )   
    Tipo_Habitacion = models.CharField(
        choices=Habitacion.TIPO_CHOICES,    
        max_length=50,
    )
    
def __str__(self):
        return f"Reserva de {self.Huespedes.nombre if self.Huespedes else 'N/A'} ({self.estado_reserva} )"