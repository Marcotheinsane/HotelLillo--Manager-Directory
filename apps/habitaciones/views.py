from django.db.models import Q
from django.core.paginator import Paginator
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import HabitacionForm
from .models import Habitacion
from apps.reservas.models import RegistroReservas  # se importa Necesariamente para detectar reservas


def consulta_habitaciones(request):
    qs = Habitacion.objects.all().order_by('numero')
    hoy = date.today()

    q = (request.GET.get('q') or '').strip()
    tipo = (request.GET.get('tipo') or '').strip()
    estado_filtro = (request.GET.get('estado') or '').strip()

    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if q:
        num_q = Q()
        if str(q).isdigit():
            num_q = Q(numero=int(q))
        qs = qs.filter(num_q | Q(tipo__icontains=q) | Q(comodidades__icontains=q))
    if tipo:
        qs = qs.filter(tipo__icontains=tipo)

    # Generar datos con lógica de ocupada / disponible / reservada / mantención
    habitaciones_data = []
    for h in qs:
        # Si está en mantención, prioridad absoluta
        if h.estado == 'MANTENCION':
            estado_real = 'Mantención'
            proxima = '—'

        else:
            # ¿Está ocupada hoy?
            reserva_activa = RegistroReservas.objects.filter(
                Habitaciones=h,
                estado_reserva__in=['confirmada', 'en_progreso'],
                fecha_check_in__lte=hoy,
                fecha_check_out__gt=hoy
            ).first()

            # ¿Tiene reserva futura?
            reserva_futura = RegistroReservas.objects.filter(
                Habitaciones=h,
                estado_reserva='confirmada',
                fecha_check_in__gt=hoy
            ).order_by('fecha_check_in').first()

            if reserva_activa:
                estado_real = 'Ocupada'
                proxima = f"Hasta {reserva_activa.fecha_check_out.strftime('%d/%m')}"
            elif reserva_futura:
                estado_real = 'Reservada'
                proxima = f"{reserva_futura.fecha_check_in.strftime('%d/%m')} - {reserva_futura.fecha_check_out.strftime('%d/%m')}"
            else:
                estado_real = 'Disponible'
                proxima = '—'

        habitaciones_data.append({
            'id': h.id,
            'numero': h.numero,
            'tipo': h.get_tipo_display(),
            'capacidad': h.capacidad,
            'tarifa': h.tarifa,
            'comodidades': h.comodidades,
            'estado': estado_real,
            'proxima_reserva': proxima
        })

    # filtrar por rango de fechas: devolver habitaciones que tengan reservas que se crucen con el rango
    if fecha_inicio and fecha_fin:
        try:
            from datetime import datetime
            fi = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            ff = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            filtered = []
            for hdata in habitaciones_data:
                reservas = RegistroReservas.objects.filter(Habitaciones_id=hdata['id'])
                # verificar si alguna reserva intersecta el rango
                intersects = reservas.filter(fecha_check_in__lte=ff, fecha_check_out__gte=fi).exists()
                if intersects:
                    filtered.append(hdata)
            habitaciones_data = filtered
        except Exception:
            from django.contrib import messages
            messages.warning(request, 'Formato de fechas inválido. Use YYYY-MM-DD.')

    # por estado después de calcular estado_real
    if estado_filtro:
        habitaciones_data = [h for h in habitaciones_data if h['estado'].upper() == estado_filtro.upper()]

    #  Paginación es como una lista ya procesada
    paginator = Paginator(habitaciones_data, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'habitaciones': page_obj,
        'page_obj': page_obj,
        'q': q,
        'tipo': tipo,
        'estado': estado_filtro,
        'fecha_inicio': fecha_inicio or '',
        'fecha_fin': fecha_fin or ''
    }
    return render(request, 'habitacion/consulta.html', context)


def registrar_habitacion(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('consultar_habitaciones')  # Cambiado para redirigir a consulta
    else:
        form = HabitacionForm()
    return render(request, 'habitacion/registrar.html', {'form': form})


def editar_habitacion(request, pk):
    from django.shortcuts import get_object_or_404
    habitacion = get_object_or_404(Habitacion, pk=pk)
    if request.method == 'POST':
        form = HabitacionForm(request.POST, instance=habitacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Habitación actualizada correctamente.')
            return redirect('consultar_habitaciones')
    else:
        form = HabitacionForm(instance=habitacion)
    return render(request, 'habitacion/editar.html', {'form': form, 'habitacion': habitacion})


def eliminar_habitacion(request, pk):
    from django.shortcuts import get_object_or_404
    habitacion = get_object_or_404(Habitacion, pk=pk)
    # Verificar reservas relacionadas
    tiene_reservas = RegistroReservas.objects.filter(Habitaciones=habitacion).exists()
    if request.method == 'POST':
        if tiene_reservas:
            # No eliminar físicamente, marcar como en mantención (anular)
            habitacion.estado = 'MANTENCION'
            habitacion.save()
            messages.warning(request, 'La habitación tiene reservas asociadas. Se marcó como Mantención (anulada).')
        else:
            habitacion.delete()
            messages.success(request, 'Habitación eliminada correctamente.')
        return redirect('consultar_habitaciones')

    return render(request, 'habitacion/confirmar_eliminar.html', {'habitacion': habitacion, 'tiene_reservas': tiene_reservas})