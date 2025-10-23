from django.db import models
from django.core.exceptions import ValidationError

class EstadoHabitacion(models.TextChoices):
    DISPONIBLE = 'DISPONIBLE', 'Disponible'
    OCUPADA = 'OCUPADA', 'Ocupada'
    MANTENCION = 'MANTENCION', 'En Mantención'

class Habitacion(models.Model):
    numero = models.IntegerField(unique=True)
    tipo = models.CharField(max_length=50)
    capacidad = models.PositiveIntegerField()
    tarifa = models.PositiveIntegerField()
    comodidades = models.TextField()
    estado = models.CharField(
        max_length=15,
        choices=EstadoHabitacion.choices,
        default=EstadoHabitacion.DISPONIBLE
    )

    def __str__(self):
        return f"Habitación {self.numero} ({self.tipo})"
    
    def clean(self):
        if self.capacidad < 1 or self.capacidad > 10:
            raise ValidationError("La capacidad debe estar entre 1 y 10 personas.")
        if self.tarifa <= 0:
            raise ValidationError("La tarifa debe ser mayor que cero.")