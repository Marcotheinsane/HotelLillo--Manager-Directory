from django.db import models

#modulos externos
from apps.usuarios.models import Huesped
#from app.habitaciones.models import Habitaciones ---cuando se implemente

class RegistroReservas(models.Model):
    ESTADO_CHOICES = [
        ("pendiente", "Pendiente"),
        ("confirmada", "Confirmada"),
        ("checkin", "Check-in"), 
        ("checkout", "Check-out"), 
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
# Este modulo del cangri aun no esta terminado entonces se referencia como cadena hace que se pueda llamar de forma tardia y no genere errores
    numero_habitacion_temporal = models.CharField(max_length=10, null=True, blank=True)
    
def __str__(self):
        return f"Reserva de {self.Huespedes.nombre if self.Huespedes else 'N/A'} ({self.estado_reserva})"