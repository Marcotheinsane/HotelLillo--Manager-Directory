from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Create your models here.


# PERFIL de empleado para empleados del hotel admin y recepcionistas del hotel lillo
#

class Perfil_empleado(models.Model):
    ROLES= (
        ('administrador','Administrador'),
        ('recepcionista','Recepcionistas'),
    )

    perfil_empleado= models.OneToOneField(User,on_delete=models.CASCADE)
    nombre= models.CharField(max_length=40)
    rol= models.CharField(max_length=40,choices=ROLES)
    rut= models.CharField(max_length=12)

    def __str__(self):
        return f"{self.perfil_empleado} - {self.nombre} - {self.rol}"

    def clean(self):
        # --- Control campos vacíos ---
        if not self.nombre:
            raise ValidationError("El nombre no puede estar vacío.")

        if not self.rut:
            raise ValidationError("El RUT no puede estar vacío.")

        # --- Longitud correcta ---
        if len(self.rut) < 8:
            raise ValidationError("El RUT debe tener al menos 8 caracteres.")

        # --- Verificar duplicidad manual (ya que no tienes unique=True) ---
        if Perfil_empleado.objects.exclude(id=self.id).filter(rut=self.rut).exists():
            raise ValidationError("El RUT ya existe en otro empleado.")

        # --- Validar rut ---
        validar_rut(self.rut)



# se valida a nivel de base de datos para ahorrar codigo y esfuerzo para implementarlo en views o fomrs
def validar_rut(rut):
    rut = rut.replace(".", "").replace("-", "").upper()
    cuerpo = rut[:-1]
    dv = rut[-1]

    suma = 0
    multiplo = 2

    for c in reversed(cuerpo):
        suma += int(c) * multiplo
        multiplo = 9 if multiplo == 7 else multiplo + 1

    esperado = str((11 - (suma % 11)) % 11)
    esperado = "K" if esperado == "10" else esperado

    if dv != esperado:
        raise ValidationError("El RUT no es válido.")
    
class Huesped(models.Model):
    TIPO_DOCUMENTO = (
        ('rut', 'RUT'),
        ('pasaporte', 'Pasaporte'),
    )
    
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOCUMENTO)
    numero_documento = models.CharField(max_length=12, unique=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    

    def __str__(self) -> str:
        return f"{self.nombre} {self.apellido}"
    
def clean(self):

    if not self.nombre:
        raise ValidationError({"nombre": "El nombre no puede estar vacío."})

    if not self.apellido:
        raise ValidationError({"apellido": "El apellido no puede estar vacío."})

    if not self.numero_documento:
        raise ValidationError({"numero_documento": "El número de documento no puede estar vacío."})

    # ---------------------------
    # DOCUMENTO SEGÚN TIPO
    # ---------------------------
    if self.tipo_documento == "rut":
        try:
            validar_rut(self.numero_documento)
        except ValidationError:
            raise ValidationError({
                "numero_documento": "El RUT ingresado no es válido."
            })

    elif self.tipo_documento == "pasaporte":
        if len(self.numero_documento) < 6:
            raise ValidationError({
                "numero_documento": "El pasaporte debe tener al menos 6 caracteres."
            })
        if self.numero_documento.isdigit():
            raise ValidationError({
                "numero_documento": "El pasaporte no puede ser solo números."
            })

    # ---------------------------
    # TELÉFONO
    # ---------------------------
    if self.telefono:
        if len(self.telefono) < 8:
            raise ValidationError({
                "telefono": "El número telefónico debe tener mínimo 8 dígitos."
            })
