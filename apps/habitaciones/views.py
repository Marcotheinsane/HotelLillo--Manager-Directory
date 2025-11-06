from django.db.models import Q
from django.core.paginator import Paginator
from datetime import date
from django.shortcuts import render, redirect

from .forms import HabitacionForm
from .models import Habitacion
from apps.reservas.models import RegistroReservas  # se importa Necesariamente para detectar reservas


def consulta_habitaciones(request):
    qs = Habitacion.objects.all().order_by('numero')
    hoy = date.today()

    q = (request.GET.get('q') or '').strip()
    tipo = (request.GET.get('tipo') or '').strip()
    estado_filtro = (request.GET.get('estado') or '').strip()

    if q:
        num_q = Q()
        if q.isdigit():
            num_q = Q(numero=int(q))
        qs = qs.filter(num_q | Q(tipo__icontains=q) | Q(comodidades__icontains=q))
    if tipo:
        qs = qs.filter(tipo__icontains=tipo)

    # Generar datos con lógica de ocupada / disponible / reservada / mantención
    habitaciones_data = []
    for h in qs:
        # Si está en mantención, prioridad absoluta nesario par a que no de errores
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
            'numero': h.numero,
            'tipo': h.get_tipo_display(),
            'capacidad': h.capacidad,
            'tarifa': h.tarifa,
            'comodidades': h.comodidades,
            'estado': estado_real,
            'proxima_reserva': proxima
        })

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