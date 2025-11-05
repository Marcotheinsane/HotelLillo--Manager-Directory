from django.db import models

#modulos externos
from apps.usuarios.models import Huesped
from apps.habitaciones.models import Habitacion


class RegistroReservas(models.Model):
    ESTADO_CHOICES = [
        ("pendiente", "Pendiente"),
        ("confirmada", "Confirmada"),
        ("cancelada", "Cancelada"),
        ("finalizada", "Finalizada"),
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
    Tipo_Habitacion = models.CharField(
        choices=Habitacion.TIPO_CHOICES,    
        max_length=50,
    )
    pago_estancia = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Monto pagado por la estancia al momento del check-in."
    )
    created_at = models.DateTimeField(auto_now_add=True) #necesario para poder ordenar las reservas por fecha de creacion
    
    def __str__(self):
            return f"Reserva de {self.Huespedes.nombre if self.Huespedes else 'N/A'} ({self.estado_reserva} )"