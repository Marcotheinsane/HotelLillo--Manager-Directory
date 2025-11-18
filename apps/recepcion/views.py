# apps/recepcion/views.py

from decimal import Decimal
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages

# Models del proyecto
from apps.reservas.models import RegistroReservas
from apps.habitaciones.models import Habitacion
from apps.servicios.models import ServicioCatalogo, ServicioConsumido, Pago
from .forms import ServicioFormSet, PagoForm

IVA_CHILE = Decimal("10.0")

def seleccionar_reserva_checkin(request):
    #Muestra SOLO las reservas que pueden hacer check-in HOY.
    # No permite check-in adelantado ni atrasado.
    hoy = timezone.now().date()

    pendientes_checkin = (
        RegistroReservas.objects.filter(
            estado_reserva='confirmada',
            fecha_check_in=hoy
        )
        .exclude(estado_reserva__in=['cancelada', 'finalizada'])
        .select_related('Huespedes', 'Habitaciones')
        .order_by('fecha_check_in')
    )

    context = {"pendientes_checkin": pendientes_checkin}
    return render(request, "recepcion/seleccionar_reserva_checkin.html", context)


def checkin_huesped(request, reserva_id):
    
    # Realiza el check-in del huésped SOLO si hoy coincide con su fecha reservada.
    # Marca reserva como 'en_progreso' y habitación como 'OCUPADA'.
    reserva = get_object_or_404(RegistroReservas, pk=reserva_id)
    hoy = timezone.now().date()

    # Solo reservas confirmadas pueden hacer check-in
    if reserva.estado_reserva != 'confirmada':
        messages.warning(request, "Esta reserva no puede hacer check-in.")
        return redirect('recepcion:seleccionar_reserva_checkin')

    # Validar check-in solo en el día exacto
    if reserva.fecha_check_in != hoy:
        messages.error(
            request,
            f"No se puede hacer check-in. "
            f"La fecha reservada es {reserva.fecha_check_in}."
        )
        return redirect('recepcion:seleccionar_reserva_checkin')

    huesped = reserva.Huespedes
    habitacion = reserva.Habitaciones

    # Calcular noches y costos usando las fechas originales de la reserva
    noches = max((reserva.fecha_check_out - reserva.fecha_check_in).days, 1)
    tarifa = getattr(habitacion, 'tarifa', Decimal('0.00'))
    total_estancia = tarifa * noches

    if request.method == 'POST':
        # No se cambia fecha_check_in (esa es la reservada)
        reserva.estado_reserva = 'en_progreso'
        reserva.pago_estancia = total_estancia
        reserva.save()

        habitacion.estado = 'OCUPADA'
        habitacion.save()

        messages.success(
            request,
            f"Check-in de {huesped.nombre} realizado exitosamente."
        )
        return redirect('recepcion:seleccionar_reserva_checkin')

    contexto = {
        'reserva': reserva,
        'huesped': huesped,
        'habitacion': habitacion,
        'noches': noches,
        'tarifa': tarifa,
        'total_estancia': total_estancia,
    }
    return render(request, 'recepcion/checkin.html', contexto)


def seleccionar_huesped(request):
    """
    Lista huéspedes actualmente alojados (check-in ya hecho).
    """
    hoy = timezone.now().date()

    activos = (
        RegistroReservas.objects.filter(
            fecha_check_in__lte=hoy,
            fecha_check_out__gte=hoy,
        )
        .exclude(Q(estado_reserva="finalizada") | Q(estado_reserva="cancelada"))
        .select_related("Huespedes", "Habitaciones")
        .order_by("-fecha_check_out")
    )

    return render(request, "recepcion/seleccionar_huesped.html", {"activos": activos})


def checkout_huesped(request, reserva_id):
    reserva = get_object_or_404(RegistroReservas, pk=reserva_id)
    habitacion = reserva.Habitaciones

    noches = max((reserva.fecha_check_out - reserva.fecha_check_in).days, 1)
    tarifa = getattr(habitacion, "tarifa", Decimal("0"))
    subtotal_habitacion = tarifa * noches

    servicios_guardados = reserva.servicios_consumidos.all()
    total_guardados = sum(s.total for s in servicios_guardados)

    form_pago = PagoForm(request.POST or None)
    formset_servicios = ServicioFormSet(request.POST or None, queryset=ServicioConsumido.objects.none())

    resumen_listo = False
    subtotal_nuevos = Decimal("0.00")
    subtotal_total = subtotal_habitacion + total_guardados
    iva = (subtotal_total * IVA_CHILE / 100).quantize(Decimal("0.01"))
    total_final = subtotal_total + iva

    if request.method == "POST" and form_pago.is_valid() and formset_servicios.is_valid():

        # Calcular total
        if "calcular_total" in request.POST:
            for form in formset_servicios:
                sc = form.cleaned_data.get("servicio_catalogo")
                cantidad = form.cleaned_data.get("cantidad") or 1
                if sc:
                    subtotal_nuevos += sc.precio_base * cantidad

            subtotal_total = subtotal_habitacion + total_guardados + subtotal_nuevos
            iva = (subtotal_total * IVA_CHILE / 100).quantize(Decimal("0.01"))
            total_final = subtotal_total + iva
            resumen_listo = True

        # Confirmar Check-Out
        elif "confirmar_checkout" in request.POST:
            # Guardar nuevos servicios
            for form in formset_servicios:
                sc = form.cleaned_data.get("servicio_catalogo")
                cantidad = form.cleaned_data.get("cantidad") or 1
                if sc:
                    ServicioConsumido.objects.create(
                        reserva=reserva,
                        servicio_catalogo=sc,
                        nombre=sc.nombre,
                        precio=sc.precio_base,
                        cantidad=cantidad
                    )

            subtotal_total = subtotal_habitacion + total_guardados
            iva = (subtotal_total * IVA_CHILE / 100).quantize(Decimal("0.01"))
            total_final = subtotal_total + iva

            Pago.objects.create(
                reserva=reserva,
                monto=total_final,
                metodo=form_pago.cleaned_data["metodo"],
                notas=form_pago.cleaned_data.get("notas", "")
            )

            reserva.pago_estancia = total_final
            reserva.estado_reserva = "finalizada"
            reserva.fecha_check_out = timezone.now().date()
            reserva.save()

            habitacion.estado = "DISPONIBLE"
            habitacion.save()

            messages.success(request, f" Check-Out completado. Total pagado: ${total_final}")
            return redirect("recepcion:seleccionar_huesped")

    context = {
        "reserva": reserva,
        "habitacion": habitacion,
        "noches": noches,
        "costo_habitacion": subtotal_habitacion,
        "servicios_guardados": servicios_guardados,
        "total_servicios_guardados": total_guardados,
        "form_pago": form_pago,
        "formset_servicios": formset_servicios,
        "iva_porcentaje": IVA_CHILE,
        "iva_calculado": iva,
        "total_final": total_final,
        "resumen_listo": resumen_listo
    }

    return render(request, "recepcion/checkout.html", context)
