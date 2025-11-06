from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date

#modelos de las apps
from apps.habitaciones.models import Habitacion
from apps.reservas.models import RegistroReservas as Reserva

@login_required
def home(request):
    #En esta vista se muestra el resumen del estado del hotel 
    #se muestran las metricas principales del hotel 
    
    hoy = date.today()
    total_habitaciones = Habitacion.objects.count()

    #ahora busco y filtro las habitaciones por estado
    habitaciones_disponibles = Habitacion.objects.filter(estado='DISPONIBLE').count()
    habitaciones_mantencion = Habitacion.objects.filter(estado='MANTENCION').count()

    #esta funcion es muy importante, ya que me permite saber cuantas habitaciones estan ocupadas hoy
    #para eso busco las reservas que esten activas hoy fitradas por el hoy
    reservas_activas_hoy = Reserva.objects.filter(
    fecha_check_in__lte=hoy,
    fecha_check_out__gt=hoy,
    estado_reserva__in=['confirmada']
).values_list('Habitaciones__id', flat=True).distinct()



    habitaciones_ocupadas = len(reservas_activas_hoy)

    checkins_pendientes = Reserva.objects.filter(
        fecha_check_in=hoy,
        estado_reserva='confirmada'
).count()
    checkouts_hoy = Reserva.objects.filter(
        fecha_check_out=hoy,
        estado_reserva='confirmada'
).count()
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