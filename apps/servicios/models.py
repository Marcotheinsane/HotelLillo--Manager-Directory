# apps/servicios/models.py
from django.db import models
from django.utils import timezone

# Referencias a modelos externos
from apps.reservas.models import RegistroReservas

class ServicioCatalogo(models.Model):
    """
    Catálogo de servicios (opcional — permite reusar servicios con precios).
    Ej: 'Desayuno', 'Lavandería', 'Minibar', etc.
    """
    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.TextField(blank=True)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - ${self.precio_base:.2f}"


class ServicioConsumido(models.Model):
    """
    Un servicio asociado a una reserva. Se usa para el historial de servicios y para calcular cobros.
    """
    reserva = models.ForeignKey(RegistroReservas, on_delete=models.CASCADE, related_name="servicios_consumidos")
    servicio_catalogo = models.ForeignKey(ServicioCatalogo, null=True, blank=True, on_delete=models.SET_NULL)
    nombre = models.CharField(max_length=200)  # nombre concreto del servicio (por si no viene del catálogo)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField(default=1)
    creado_en = models.DateTimeField(default=timezone.now)
    comentario = models.TextField(blank=True)

    @property
    def total(self):
        return self.precio * self.cantidad

    def __str__(self):
        return f"{self.nombre} x{self.cantidad} (${self.total:.2f})"


class Pago(models.Model):
    """
    Registro de pagos realizados en check-out (o pagos parciales si se quisiera).
    """
    METODOS = (
        ("efectivo", "Efectivo"),
        ("tarjeta", "Tarjeta"),
        ("transferencia", "Transferencia"),
        ("otro", "Otro"),
    )

    reserva = models.ForeignKey(RegistroReservas, on_delete=models.CASCADE, related_name="pagos")
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    metodo = models.CharField(max_length=30, choices=METODOS, default="efectivo")
    notas = models.TextField(blank=True)
    creado_en = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Pago ${self.monto:.2f} - {self.get_metodo_display()} ({self.creado_en.date()})"
