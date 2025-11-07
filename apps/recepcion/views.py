# apps/recepcion/views.py
from decimal import Decimal
from django.db.models import Q
from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from decimal import Decimal


# Models del proyecto
from apps.reservas.models import RegistroReservas
from apps.habitaciones.models import Habitacion
from apps.servicios.models import ServicioCatalogo, ServicioConsumido, Pago
from .forms import ServicioFormSet, PagoForm

#check in

IVA_CHILE= Decimal("10.0")

def seleccionar_reserva_checkin(request):
    """
    Lista de reservas confirmadas que pueden hacer check-in hoy o antes (no finalizadas ni canceladas).
    """
    from django.utils import timezone
    hoy = timezone.now().date()

    pendientes_checkin = (
        RegistroReservas.objects.filter(
            estado_reserva='confirmada',
            fecha_check_in__lte=hoy
        )
        .exclude(estado_reserva__in=['cancelada', 'finalizada'])
        .select_related('Huespedes', 'Habitaciones')
        .order_by('fecha_check_in')
    )

    return render(
        request,
        'recepcion/seleccionar_reserva_checkin.html',
        {'pendientes_checkin': pendientes_checkin},
    )


def checkin_huesped(request, reserva_id):
    """
    Permite registrar la llegada (check-in) de un huésped.
    Marca la reserva como 'en_progreso' y la habitación como 'OCUPADA'.
    """
    reserva = get_object_or_404(RegistroReservas, pk=reserva_id)

    # Solo reservas confirmadas pueden hacer check-in
    if reserva.estado_reserva != 'confirmada':
        messages.warning(request, "Esta reserva no puede hacer check-in.")
        return redirect('recepcion:seleccionar_reserva_checkin')

    huesped = reserva.Huespedes
    habitacion = reserva.Habitaciones

    # Calcular noches y costos 
    noches = max((reserva.fecha_check_out - reserva.fecha_check_in).days, 1)
    tarifa = getattr(habitacion, 'tarifa', Decimal('00.000'))
    total_estancia = tarifa * noches

    if request.method == 'POST':
        reserva.estado_reserva = 'en_progreso'
        reserva.fecha_check_in = timezone.now().date()
        reserva.pago_estancia = total_estancia
        reserva.save()

        habitacion.estado = 'OCUPADA'
        habitacion.save()

        messages.success(request, f"Check-in de {huesped.nombre} realizado exitosamente.")
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

def seleccionar_reserva_checkin(request):
    """
    Muestra las reservas pendientes de check-in (fecha de entrada = hoy)
    que aún no están finalizadas ni canceladas.
    """
    hoy = date.today()

    pendientes_checkin = RegistroReservas.objects.filter(
        estado_reserva__in=["pendiente", "confirmada"],  # Reservas activas
        fecha_check_in__lte=hoy,   # Ya pueden hacer check-in
        fecha_check_out__gt=hoy    # Aún no salieron
    ).select_related("Huespedes", "Habitaciones")

    context = {"pendientes_checkin": pendientes_checkin}
    return render(request, "recepcion/seleccionar_reserva_checkin.html", context)


def seleccionar_huesped(request):
    """
    Lista de huéspedes actualmente alojados (check-in activo).
    Criterio: reservas con fecha_check_in <= hoy <= fecha_check_out,
    excluyendo finalizadas/canceladas.
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

    # Variables para mostrar en template si se presiona "Calcular"
    resumen_listo = False
    subtotal_nuevos = Decimal("0.00")
    subtotal_total = subtotal_habitacion + total_guardados
    iva = (subtotal_total * IVA_CHILE / 100).quantize(Decimal("0.01"))
    total_final = subtotal_total + iva

    if request.method == "POST" and form_pago.is_valid() and formset_servicios.is_valid():

        # Si se presionó "Calcular Total"
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

        # Si se presionó "Confirmar Check-Out"
        elif "confirmar_checkout" in request.POST:
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

            messages.success(request, f"✅ Check-Out completado. Total pagado: ${total_final}")
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
