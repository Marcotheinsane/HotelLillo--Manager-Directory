from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date

from apps.habitaciones.models import Habitacion
from apps.reservas.models import RegistroReservas as Reserva

@login_required
def home(request):
    hoy = date.today()
    
    # ========== MÉTRICAS PRINCIPALES ==========
    
    # Total de habitaciones
    total_habitaciones = Habitacion.objects.count()
    
    # Habitaciones con estado DISPONIBLE
    habitaciones_disponibles = Habitacion.objects.filter(estado='DISPONIBLE').count()
    
    # Habitaciones en mantención
    habitaciones_mantencion = Habitacion.objects.filter(estado='MANTENCION').count()
    
    # 👇 HABITACIONES REALMENTE OCUPADAS (con reservas activas HOY)
    reservas_activas_hoy = Reserva.objects.filter(
        fecha_check_in__lte=hoy,
        fecha_check_out__gt=hoy,
        estado_reserva__in=['confirmada']
    ).values_list('Habitaciones__id', flat=True).distinct()
    
    habitaciones_ocupadas = len(reservas_activas_hoy)
    
    # Check-ins pendientes para hoy
    checkins_pendientes = Reserva.objects.filter(
        fecha_check_in=hoy,
        estado_reserva='confirmada'
    ).count()
    
    # Check-outs para hoy
    checkouts_hoy = Reserva.objects.filter(
        fecha_check_out=hoy,
        estado_reserva='confirmada'
    ).count()
    
    # Reservas pendientes de confirmación
    reservas_pendientes = Reserva.objects.filter(
        estado_reserva='pendiente'
    ).count()
    
    context = {
        'total_habitaciones': total_habitaciones,
        'habitaciones_ocupadas': habitaciones_ocupadas,
        'habitaciones_disponibles': habitaciones_disponibles,
        'habitaciones_mantencion': habitaciones_mantencion,
        'checkins_pendientes': checkins_pendientes,
        'checkouts_hoy': checkouts_hoy,
        'reservas_pendientes': reservas_pendientes,
    }
    
    return render(request, 'home.html', context)