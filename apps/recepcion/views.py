from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone # Usaremos timezone para la fecha actual
from django.db.models import Q # Para construir consultas complejas

# models
from apps.reservas.models import RegistroReservas
from apps.usuarios.models import Huesped
from apps.habitaciones.models import Habitacion

# forms
from .forms import CheckoutForm, ServiceFormSet


def seleccionar_huesped(request):
	"""Lista de huéspedes actualmente alojados (check-in activo).
	Definición asumida: reservas con fecha_check_in <= hoy < fecha_check_out y estado_reserva == 'confirmada'.
	"""
	# Obtiene solo las reservas de huéspedes que están actualmente en el hotel.
	hoy = timezone.now().date()
	activos = RegistroReservas.objects.filter(
		fecha_check_in__lte=hoy,
		fecha_check_out__gte=hoy,
	).exclude(
		Q(estado_reserva='finalizada') | Q(estado_reserva='cancelada')
	).select_related('Huespedes', 'Habitaciones').order_by('-fecha_check_out')

	return render(request, 'recepcion/seleccionar_huesped.html', {'activos': activos})

def checkout_huesped(request, reserva_id):
	reserva = get_object_or_404(RegistroReservas, pk=reserva_id)
	huesped = reserva.Huespedes
	habitacion = reserva.Habitaciones

	# calcular noches
	noches = (reserva.fecha_check_out - reserva.fecha_check_in).days
	if noches <= 0:
		noches = 1

	habitacion_tarifa = getattr(habitacion, 'tarifa', 0)
	costo_habitacion = noches * habitacion_tarifa

	# --- Lógica de Pago en Check-in ---
	# Si el campo pago_estancia está en cero, lo actualizamos con el costo de la habitación.
	# Esto simula que el pago se realizó al momento del check-in.
	if request.method == 'POST':
		form = CheckoutForm(request.POST)
		service_formset = ServiceFormSet(request.POST)
		if form.is_valid() and service_formset.is_valid():
			# Obtenemos el porcentaje de impuestos como Decimal para mantener la precisión.
			from decimal import Decimal
			impuestos_pct_decimal = form.cleaned_data.get('impuestos')
			impuestos_pct = impuestos_pct_decimal if impuestos_pct_decimal is not None else Decimal('0.0')

			notas = form.cleaned_data.get('notas')

			servicios = []
			total_servicios = 0
			for f in service_formset:
				nombre = f.cleaned_data.get('nombre')
				precio = f.cleaned_data.get('precio') or 0
				if nombre and precio:
					servicios.append({'nombre': nombre, 'precio': precio})
					total_servicios += precio

			# El subtotal a pagar en checkout es SOLO de los servicios.
			subtotal = total_servicios
			impuestos = (subtotal * impuestos_pct) / Decimal('100')
			total_a_pagar_checkout = subtotal + impuestos # El cálculo es correcto

			# --- Lógica de confirmación de Check-Out ---
			if 'confirmar_checkout' in request.POST:
				# 1. Actualizar y guardar la reserva
				reserva.estado_reserva = 'finalizada'
				reserva.fecha_check_out = timezone.now().date()
				# Opcional: Aquí podrías guardar el total de la factura si tuvieras un campo para ello.
				reserva.save()

				# 2. Liberar la habitación
				habitacion.estado = 'disponible'
				habitacion.save()

				# 3. Redirigir con un mensaje de éxito (descomentar si tienes `messages` configurado)
				# from django.contrib import messages
				# messages.success(request, f"Check-out de {huesped.nombre} completado exitosamente.")
				return redirect('recepcion:seleccionar_huesped')

			# Renderizar resumen final en la misma plantilla (no persistimos)
			contexto = {
				'reserva': reserva,
				'huesped': huesped,
				'habitacion': habitacion,
				'noches': noches,
				'costo_habitacion': costo_habitacion,
				'pago_estancia': reserva.pago_estancia, # Mostramos lo que ya se pagó
				'servicios': servicios,
				'total_servicios': total_servicios,
				'impuestos_pct': impuestos_pct,
				'impuestos_calculados': impuestos, # Renombramos para evitar conflicto con el campo del form
				'total_a_pagar_checkout': total_a_pagar_checkout,
				'notas': notas,
				'form': form,
				'service_formset': service_formset,
				'resumen_listo': True, # Bandera para mostrar el resumen y el botón de confirmar
			}
			return render(request, 'recepcion/checkout.html', contexto)
	else:
		form = CheckoutForm()
		service_formset = ServiceFormSet()

	contexto = {
		'reserva': reserva,
		'huesped': huesped,
		'habitacion': habitacion,
		'noches': noches,
		'costo_habitacion': costo_habitacion,
		# Si el pago de la estancia aún no se ha registrado, se calcula y muestra.
		# Se guardará en la BD solo al confirmar el check-out (o en un futuro check-in).
		'pago_estancia': reserva.pago_estancia,
		'form': form,
		'service_formset': service_formset,
	}
	return render(request, 'recepcion/checkout.html', contexto)
