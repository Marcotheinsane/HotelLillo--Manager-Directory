from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Habitacion
from .forms import HabitacionForm
from decimal import Decimal


class HabitacionModelTests(TestCase):
    """Tests para el modelo Habitacion"""

    def setUp(self):
        """Crear datos de prueba"""
        self.hab1 = Habitacion.objects.create(
            numero=101,
            tipo='SIMPLE',
            capacidad=2,
            tarifa=Decimal('50000.00'),
            comodidades='WiFi, TV'
        )

    # ===== PRUEBAS DE DUPLICIDAD (5 ptos) =====
    def test_numero_unico(self):
        """Control de duplicidad: No se puede crear dos habitaciones con el mismo número"""
        with self.assertRaises(Exception):  # IntegrityError o similar
            Habitacion.objects.create(
                numero=101,  # Ya existe
                tipo='DOBLE',
                capacidad=2,
                tarifa=Decimal('60000.00'),
                comodidades='WiFi, TV, Jacuzzi'
            )

    def test_numero_unico_en_formulario(self):
        """Form: Control de duplicidad en formulario"""
        form = HabitacionForm(data={
            'numero': '101',  # Ya existe
            'tipo': 'DOBLE',
            'capacidad': 2,
            'tarifa': '60000.00',
            'comodidades': 'WiFi',
            'estado': 'DISPONIBLE'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Ya existe una habitación con ese número', str(form.errors))

    # ===== PRUEBAS DE CAMPO VACÍO (5 ptos) =====
    def test_numero_requerido(self):
        """Número no puede estar vacío"""
        form = HabitacionForm(data={
            'numero': '',
            'tipo': 'SIMPLE',
            'capacidad': 2,
            'tarifa': '50000.00',
            'comodidades': 'WiFi',
            'estado': 'DISPONIBLE'
        })
        self.assertFalse(form.is_valid())

    def test_tarifa_requerida(self):
        """Tarifa no puede estar vacía"""
        form = HabitacionForm(data={
            'numero': '102',
            'tipo': 'SIMPLE',
            'capacidad': 2,
            'tarifa': '',
            'comodidades': 'WiFi',
            'estado': 'DISPONIBLE'
        })
        self.assertFalse(form.is_valid())

    def test_capacidad_requerida(self):
        """Capacidad no puede estar vacía"""
        form = HabitacionForm(data={
            'numero': '102',
            'tipo': 'SIMPLE',
            'capacidad': '',
            'tarifa': '50000.00',
            'comodidades': 'WiFi',
            'estado': 'DISPONIBLE'
        })
        self.assertFalse(form.is_valid())

    # ===== PRUEBAS DE TIPOS DE DATOS (5 pts) =====
    def test_numero_debe_ser_numerico(self):
        """Número debe ser numérico, no texto"""
        form = HabitacionForm(data={
            'numero': 'ABC123',
            'tipo': 'SIMPLE',
            'capacidad': 2,
            'tarifa': '50000.00',
            'comodidades': 'WiFi',
            'estado': 'DISPONIBLE'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('El número debe ser numérico', str(form.errors))

    def test_tarifa_debe_ser_decimal(self):
        """Tarifa debe ser número decimal positivo"""
        form = HabitacionForm(data={
            'numero': '102',
            'tipo': 'SIMPLE',
            'capacidad': 2,
            'tarifa': 'no_es_numero',
            'comodidades': 'WiFi',
            'estado': 'DISPONIBLE'
        })
        self.assertFalse(form.is_valid())

    def test_tarifa_debe_ser_positiva(self):
        """Tarifa debe ser mayor que cero"""
        form = HabitacionForm(data={
            'numero': '102',
            'tipo': 'SIMPLE',
            'capacidad': 2,
            'tarifa': '0',  # O tarifa negativa
            'comodidades': 'WiFi',
            'estado': 'DISPONIBLE'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('debe ser mayor que cero', str(form.errors))

    def test_capacidad_debe_ser_positiva(self):
        """Capacidad debe estar entre 1 y 10 personas"""
        hab = Habitacion(
            numero=999,
            tipo='SIMPLE',
            capacidad=0,  # Inválido
            tarifa=Decimal('50000.00'),
            comodidades='WiFi'
        )
        with self.assertRaises(ValidationError):
            hab.full_clean()

    # ===== PRUEBAS DE LONGITUD DE CAMPOS (5 ptos) =====
    def test_longitud_comodidades_maxima(self):
        """Comodidades no debe exceder 500 caracteres"""
        form = HabitacionForm(data={
            'numero': '102',
            'tipo': 'SIMPLE',
            'capacidad': 2,
            'tarifa': '50000.00',
            'comodidades': 'x' * 501,  # Más de 500 caracteres
            'estado': 'DISPONIBLE'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('máximo 500 caracteres', str(form.errors))

    def test_tipo_habitacion_valido(self):
        """Tipo debe estar en las opciones definidas"""
        form = HabitacionForm(data={
            'numero': '102',
            'tipo': 'TIPO_INVALIDO',
            'capacidad': 2,
            'tarifa': '50000.00',
            'comodidades': 'WiFi',
            'estado': 'DISPONIBLE'
        })
        self.assertFalse(form.is_valid())

    def test_estado_valido(self):
        """Estado debe estar en las opciones definidas"""
        form = HabitacionForm(data={
            'numero': '102',
            'tipo': 'SIMPLE',
            'capacidad': 2,
            'tarifa': '50000.00',
            'comodidades': 'WiFi',
            'estado': 'ESTADO_INVALIDO'
        })
        self.assertFalse(form.is_valid())

    # ===== PRUEBAS DE INTEGRIDAD REFERENCIAL (5 ptos) =====
    def test_habitacion_con_estado_por_defecto(self):
        """Una habitación nueva debe tener estado DISPONIBLE por defecto"""
        hab = Habitacion.objects.create(
            numero=200,
            tipo='DOBLE',
            capacidad=2,
            tarifa=Decimal('70000.00'),
            comodidades='WiFi, TV, Aire'
        )
        self.assertEqual(hab.estado, 'DISPONIBLE')

    def test_relacion_con_reservas(self):
        """Una habitación puede tener varias reservas asociadas (FK)"""
        from apps.reservas.models import RegistroReservas
        from apps.usuarios.models import Huesped
        from datetime import date
        
        # Crear un huésped
        huesped = Huesped.objects.create(
            rut='12345678-9',
            nombre='Juan Pérez',
            email='juan@example.com'
        )
        
        # Crear una reserva asociada a esta habitación
        reserva = RegistroReservas.objects.create(
            Huespedes=huesped,
            Habitaciones=self.hab1,
            Tipo_Habitacion='SIMPLE',
            fecha_check_in=date.today(),
            fecha_check_out=date(2025, 12, 20),
            estado_reserva='confirmada'
        )
        
        # Verificar que la relación existe
        self.assertEqual(reserva.Habitaciones.numero, self.hab1.numero)
        self.assertTrue(RegistroReservas.objects.filter(Habitaciones=self.hab1).exists())

    def test_validacion_capacidad_rango(self):
        """Capacidad debe estar entre 1 y 10"""
        # Menor a 1
        hab = Habitacion(
            numero=999,
            tipo='SIMPLE',
            capacidad=0,
            tarifa=Decimal('50000.00'),
            comodidades='WiFi'
        )
        with self.assertRaises(ValidationError):
            hab.full_clean()
        
        # Mayor a 10
        hab2 = Habitacion(
            numero=998,
            tipo='SIMPLE',
            capacidad=11,
            tarifa=Decimal('50000.00'),
            comodidades='WiFi'
        )
        with self.assertRaises(ValidationError):
            hab2.full_clean()

    def test_validacion_tarifa_cero(self):
        """Tarifa no puede ser cero o negativa"""
        hab = Habitacion(
            numero=997,
            tipo='SIMPLE',
            capacidad=2,
            tarifa=Decimal('-1000.00'),  # Negativa
            comodidades='WiFi'
        )
        with self.assertRaises(ValidationError):
            hab.full_clean()


class HabitacionFormTests(TestCase):
    """Tests específicos para el formulario"""

    def test_formulario_valido(self):
        """Formulario válido con todos los datos correctos"""
        form = HabitacionForm(data={
            'numero': '301',
            'tipo': 'SUITE',
            'capacidad': 4,
            'tarifa': '150000.00',
            'comodidades': 'WiFi, Smart TV, Jacuzzi, Vista al mar',
            'estado': 'DISPONIBLE'
        })
        self.assertTrue(form.is_valid())

    def test_numero_positivo(self):
        """Número debe ser mayor a cero"""
        form = HabitacionForm(data={
            'numero': '-5',
            'tipo': 'SIMPLE',
            'capacidad': 2,
            'tarifa': '50000.00',
            'comodidades': 'WiFi',
            'estado': 'DISPONIBLE'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('mayor que cero', str(form.errors))

    def test_editar_habitacion_mantiene_validacion(self):
        """Al editar, se valida igual que al crear (pero permite el número actual)"""
        hab = Habitacion.objects.create(
            numero=401,
            tipo='SIMPLE',
            capacidad=2,
            tarifa=Decimal('50000.00'),
            comodidades='WiFi'
        )
        
        # Editar con el mismo número debe ser válido
        form = HabitacionForm(
            data={
                'numero': '401',  # Mismo número
                'tipo': 'DOBLE',
                'capacidad': 2,
                'tarifa': '60000.00',
                'comodidades': 'WiFi, TV',
                'estado': 'DISPONIBLE'
            },
            instance=hab
        )
        self.assertTrue(form.is_valid())
