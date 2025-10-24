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
    
    # NUEVO CAMPO: Para registrar el motivo de la cancelación
    motivo_cancelacion = models.TextField(
        blank=True,    # Permite que el campo esté vacío
        null=True,     # Permite valor NULL en la base de datos
        help_text="Motivo por el cual se canceló la reserva."
    )
    
    Huespedes =  models.ForeignKey(
        Huesped,
        on_delete=models.CASCADE
    )
    Habitaciones = models.ForeignKey(
        Habitacion,
        on_delete=models.CASCADE,
        null = True,
        blank= True,
    )
    Estado_Habitacion =models.CharField(
        choices=Habitacion.ESTADO_CHOICES,
        max_length=15,
        default="disponible"
    )
    
def _str_(self):
        return f"Reserva de {self.Huespedes.nombre if self.Huespedes else 'N/A'} ({self.estado_reserva} )"
    
