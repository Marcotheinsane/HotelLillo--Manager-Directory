from django.db import models
<<<<<<< HEAD
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
=======
from django.core.exceptions import ValidationError  # Import necesario para validaciones

class EstadoHabitacion(models.TextChoices):
    DISPONIBLE = 'Disponible', 'Disponible'
    OCUPADA = 'Ocupada', 'Ocupada'
    LIMPIEZA = 'Limpieza', 'Limpieza'
    MANTENCION = 'Mantenimiento', 'Mantenimiento'

class Habitacion(models.Model):
    numero = models.IntegerField(unique=True)
    tipo = models.CharField(max_length=50)
>>>>>>> 23b9575 (Avance CRUD con función de registro)
    capacidad = models.PositiveIntegerField()
    tarifa = models.PositiveIntegerField()
    comodidades = models.TextField()
    estado = models.CharField(
        max_length=15,
<<<<<<< HEAD
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
        
=======
        choices=EstadoHabitacion.choices,
        default=EstadoHabitacion.DISPONIBLE
    )

    def __str__(self):
        return f"Habitación {self.numero} ({self.tipo})"

    def clean(self):
        """
        Validaciones de modelo. Se ejecutan con form.save() o model.full_clean().
        """
        # Validar Capacidad
        if self.capacidad < 1 or self.capacidad > 10:
            raise ValidationError("La capacidad debe estar entre 1 y 10 personas.")

        # Validar Tarifa
        if self.tarifa <= 0:
            raise ValidationError({'tarifa': "La tarifa debe ser mayor que cero."})
>>>>>>> 23b9575 (Avance CRUD con función de registro)
