from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Rol(models.Model):
    """
    Roles de usuarios en el sistema
    """
    TIPOS_ROL = [
        ('ADMIN', 'Administrador'),
        ('RECEP', 'Recepcionista'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_rol = models.CharField(max_length=10, choices=TIPOS_ROL, default='RECEP')
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_tipo_rol_display()}"


class TipoHabitacion(models.Model):
    """
    Catálogo de tipos de habitaciones
    """
    TIPOS = [
        ('SUITE', 'Suite con Jacuzzi'),
        ('MATRIMONIAL', 'Habitación Matrimonial Estándar'),
        ('TWIN', 'Habitación Twin (2 camas)'),
        ('FAMILIAR', 'Habitación Familiar'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPOS, unique=True)
    descripcion = models.TextField(blank=True)
    capacidad_maxima = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    
    def __str__(self):
        return self.get_tipo_display()


class Habitacion(models.Model):
    """
    HU02, HU03, HU04, HU05: Gestión de habitaciones
    """
    ESTADOS = [
        ('DISPONIBLE', 'Disponible'),
        ('OCUPADA', 'Ocupada'),
        ('LIMPIEZA', 'En Limpieza'),
        ('MANTENIMIENTO', 'En Mantenimiento'),
    ]
    
    VISTAS = [
        ('MAR', 'Vista al Mar'),
        ('CERRO', 'Vista al Cerro'),
        ('INTERIOR', 'Interior'),
    ]
    
    numero = models.CharField(max_length=10, unique=True)
    tipo = models.ForeignKey(TipoHabitacion, on_delete=models.PROTECT)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='DISPONIBLE')
    precio_base = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    vista = models.CharField(max_length=10, choices=VISTAS, default='INTERIOR')
    tiene_balcon = models.BooleanField(default=False)
    comodidades = models.TextField()
    observaciones = models.TextField(blank=True)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Hab. {self.numero} - {self.tipo.get_tipo_display()}"


class Huesped(models.Model):
    """
    HU13, HU14, HU15: Gestión de huéspedes
    """
    TIPO_DOCUMENTO = [
        ('RUT', 'RUT'),
        ('PASAPORTE', 'Pasaporte'),
        ('DNI', 'DNI'),
    ]
    
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOCUMENTO)
    numero_documento = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=255, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    preferencias = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.numero_documento})"
    
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"


class Reserva(models.Model):
    """
    HU06, HU07, HU08, HU09: Gestión de reservas
    """
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CHECKIN', 'Check-in Realizado'),
        ('CHECKOUT', 'Check-out Realizado'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    codigo = models.CharField(max_length=20, unique=True)
    huesped = models.ForeignKey(Huesped, on_delete=models.PROTECT, related_name='reservas')
    habitacion = models.ForeignKey(Habitacion, on_delete=models.PROTECT, related_name='reservas')
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    numero_personas = models.IntegerField(validators=[MinValueValidator(1)])
    estado = models.CharField(max_length=15, choices=ESTADOS, default='PENDIENTE')
    requiere_estacionamiento = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True)
    motivo_cancelacion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reservas_creadas')
    
    def __str__(self):
        return f"Reserva {self.codigo} - {self.huesped.nombre_completo()}"
    
    def calcular_noches(self):
        return (self.fecha_salida - self.fecha_entrada).days


class Acompanante(models.Model):
    """
    Acompañantes de una reserva
    """
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='acompanantes')
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=10, choices=Huesped.TIPO_DOCUMENTO)
    numero_documento = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class CheckIn(models.Model):
    """
    HU10: Registro de check-in
    """
    reserva = models.OneToOneField(Reserva, on_delete=models.PROTECT)
    fecha_hora = models.DateTimeField(default=timezone.now)
    observaciones = models.TextField(blank=True)
    realizado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"Check-in - {self.reserva.codigo}"


class ServicioAdicional(models.Model):
    """
    Catálogo de servicios adicionales
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio}"


class ConsumoServicio(models.Model):
    """
    HU16: Registro de servicios adicionales consumidos
    """
    reserva = models.ForeignKey(Reserva, on_delete=models.PROTECT, related_name='consumos')
    servicio = models.ForeignKey(ServicioAdicional, on_delete=models.PROTECT)
    cantidad = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_hora = models.DateTimeField(default=timezone.now)
    observaciones = models.TextField(blank=True)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.servicio.nombre} - {self.reserva.codigo}"
    
    def calcular_total(self):
        return self.cantidad * self.precio_unitario


class CheckOut(models.Model):
    """
    HU11, HU12: Registro de check-out y facturación
    """
    reserva = models.OneToOneField(Reserva, on_delete=models.PROTECT)
    fecha_hora = models.DateTimeField(default=timezone.now)
    total_habitacion = models.DecimalField(max_digits=10, decimal_places=2)
    total_servicios = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_final = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.TextField(blank=True)
    realizado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"Check-out - {self.reserva.codigo}"


class HistorialCambio(models.Model):
    """
    Auditoría de cambios en el sistema
    """
    TIPOS_ENTIDAD = [
        ('HABITACION', 'Habitación'),
        ('RESERVA', 'Reserva'),
        ('HUESPED', 'Huésped'),
    ]
    
    TIPOS_ACCION = [
        ('CREAR', 'Crear'),
        ('MODIFICAR', 'Modificar'),
        ('ELIMINAR', 'Eliminar'),
    ]
    
    tipo_entidad = models.CharField(max_length=20, choices=TIPOS_ENTIDAD)
    id_entidad = models.IntegerField()
    tipo_accion = models.CharField(max_length=10, choices=TIPOS_ACCION)
    descripcion = models.TextField()
    fecha_hora = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.get_tipo_accion_display()} - {self.get_tipo_entidad_display()} - {self.fecha_hora}"