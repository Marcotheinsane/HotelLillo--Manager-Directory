from django.db import models
from django.core.exceptions import ValidationError

class Habitacion(models.Model):
    ESTADO_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('OCUPADA', 'Ocupada'),
        ('MANTENCION', 'En Mantención'),
    ]
    
    TIPO_CHOICES = [
        ('SENCILLA', 'Sencilla'),
        ('DOBLE', 'Doble'),
        ('SUITE', 'Suite'),
    ]
    
    numero = models.IntegerField(unique=True)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    capacidad = models.PositiveIntegerField()
    tarifa = models.PositiveIntegerField()
    comodidades = models.TextField()
    estado = models.CharField(
        max_length=15,
        choices=ESTADO_CHOICES,
        default='DISPONIBLE'
    )

    def _str_(self):
        return f"Habitación {self.numero} ({self.tipo})"

    def clean(self):
        #validaciones personalizadas para el modelo Habitacion
        # Validar Capacidad 
        if self.capacidad < 1 or self.capacidad > 10:
            raise ValidationError("La capacidad debe estar entre 1 y 10 personas.")

        # Validar Tarifa 
        if self.tarifa <= 0:
            raise ValidationError({'tarifa': "La tarifa debe ser mayor que cero."})
        