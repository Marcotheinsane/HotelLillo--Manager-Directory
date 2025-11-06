# apps/recepcion/views.py
from decimal import Decimal
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

# Models del proyecto
from apps.reservas.models import RegistroReservas
from apps.usuarios.models import Huesped
from apps.habitaciones.models import Habitacion

# NUEVO: modelos de cobros/servicios
from apps.servicios.models import ServicioConsumido, Pago

# Formularios
from .forms import CheckoutForm, ServiceFormSet


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
    """
    Flujo de checkout:
    - GET: muestra historial de servicios + formset para agregar nuevos.
    - POST (previsualizar): calcula totales pero NO persiste.
    - POST (confirmar_checkout): crea ServicioConsumido, registra Pago, finaliza reserva y libera habitación.
    Reglas actuales:
    - Se cobra SOLO servicios (no incluye costo de habitación en el cobro de checkout).
    - `pago_estancia` se deja como está (puedes activar el acumulado si lo deseas).
    """
    reserva = get_object_or_404(RegistroReservas, pk=reserva_id)
    huesped = reserva.Huespedes
    habitacion = reserva.Habitaciones

    # Calcular noches (mínimo 1)
   # Calcular noches (mínimo 1)
    noches = (reserva.fecha_check_out - reserva.fecha_check_in).days
    noches = max(1, noches)
    habitacion.estado = "DISPONIBLE"  # no "disponible"
    habitacion.save()


    # En tu proyecto la tarifa de habitación está en 'tarifa'
    habitacion_tarifa = getattr(habitacion, "tarifa", 0) or 0
    costo_habitacion = noches * habitacion_tarifa

    # Historial previamente guardado
    servicios_guardados = reserva.servicios_consumidos.all().order_by("-creado_en")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        service_formset = ServiceFormSet(request.POST)

        if form.is_valid() and service_formset.is_valid():
            impuestos_pct = form.cleaned_data.get("impuestos") or Decimal("0.0")
            notas = form.cleaned_data.get("notas", "")
            metodo_pago = (form.cleaned_data.get("metodo_pago") or "efectivo").strip()

            # Construimos lista de servicios nuevos (NO persistimos aún)
            servicios_nuevos = []
            subtotal_nuevos = Decimal("0.00")

            for f in service_formset:
                if not f.cleaned_data or f.cleaned_data.get("DELETE"):
                    continue
                nombre = f.cleaned_data.get("nombre")
                precio = f.cleaned_data.get("precio")
                cantidad = f.cleaned_data.get("cantidad") or 1
                if nombre and precio:
                    precio_dec = Decimal(precio)
                    cantidad_int = int(cantidad)
                    servicios_nuevos.append(
                        {
                            "nombre": nombre,
                            "precio": precio_dec,
                            "cantidad": cantidad_int,
                            "total": precio_dec * cantidad_int,
                        }
                    )
                    subtotal_nuevos += precio_dec * cantidad_int

            impuestos_calculados = (subtotal_nuevos * impuestos_pct) / Decimal("100")
            total_a_pagar_checkout = (subtotal_nuevos + impuestos_calculados).quantize(
                Decimal("0.01")
            )

            # --- Confirmación: aquí sí persistimos ---
            if "confirmar_checkout" in request.POST:
                # 1) Guardar cada servicio consumido
                for item in servicios_nuevos:
                    ServicioConsumido.objects.create(
                        reserva=reserva,
                        nombre=item["nombre"],
                        precio=item["precio"],
                        cantidad=item["cantidad"],
                    )

                # 2) Registrar el pago si corresponde
                if total_a_pagar_checkout > 0:
                    Pago.objects.create(
                        reserva=reserva,
                        monto=total_a_pagar_checkout,
                        metodo=metodo_pago,
                        notas=f"Pago confirmado en check-out. {notas}".strip(),
                    )
                    # (Opcional) acumular en pago_estancia:
                    # reserva.pago_estancia = (Decimal(reserva.pago_estancia or 0) + total_a_pagar_checkout)

                # 3) Finalizar la reserva y liberar habitación
                reserva.estado_reserva = "finalizada"
                reserva.fecha_check_out = timezone.now().date()
                # Si activaste el acumulado en pago_estancia, no olvides guardar ese valor también.
                reserva.save()

                habitacion.estado = "disponible"
                habitacion.save()

                return redirect("recepcion:seleccionar_huesped")

            # Previsualización (NO guarda)
            contexto = {
                "reserva": reserva,
                "huesped": huesped,
                "habitacion": habitacion,
                "noches": noches,
                "costo_habitacion": costo_habitacion,
                "pago_estancia": reserva.pago_estancia,

                "servicios_guardados": servicios_guardados,
                "servicios": servicios_nuevos,  # lo nuevo (preview)
                "total_servicios": subtotal_nuevos,
                "impuestos_pct": impuestos_pct,
                "impuestos_calculados": impuestos_calculados,
                "total_a_pagar_checkout": total_a_pagar_checkout,

                "notas": notas,
                "form": form,
                "service_formset": service_formset,
                "resumen_listo": True,
            }
            return render(request, "recepcion/checkout.html", contexto)

    else:
        form = CheckoutForm()
        service_formset = ServiceFormSet()

    # GET inicial
    contexto = {
        "reserva": reserva,
        "huesped": huesped,
        "habitacion": habitacion,
        "noches": noches,
        "costo_habitacion": costo_habitacion,
        "pago_estancia": reserva.pago_estancia,

        "servicios_guardados": servicios_guardados,

        "form": form,
        "service_formset": service_formset,
    }
    return render(request, "recepcion/checkout.html", contexto)



