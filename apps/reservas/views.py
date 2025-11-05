from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from datetime import datetime

from apps.reservas.models import RegistroReservas
from .forms import FormularioReservas
from apps.habitaciones.models import Habitacion


def Registrar_reserva(request):
    if request.method == "POST":
        form = FormularioReservas(request.POST)
        if form.is_valid():
            reserva = form.save()  # Guardamos la reserva     
            messages.success(request, f"Reserva para {reserva.Huespedes.nombre} creada exitosamente.")
            return redirect('reservas:listar_reservas')
    else:
        form = FormularioReservas()

    return render(request, 'Reservas/Registro_reservas.html', {'form': form})


def listar_reservas(request):
    #se usa select_related para optimizar consultas de lo contrario haria muchas consultas a la bd 
    reservas = RegistroReservas.objects.select_related('Huespedes', 'Habitaciones').order_by('-fecha_check_in')
    return render(request, 'Reservas/listar_reservas.html', {'reservas': reservas})


def confirmar_reserva(request, pk):
    reserva = get_object_or_404(RegistroReservas, pk=pk)
    if reserva.estado_reserva == 'pendiente':
        reserva.estado_reserva = 'confirmada'
        reserva.save()
        messages.success(request, f"Reserva #{reserva.id} confirmada exitosamente.")
    else:
        messages.warning(request, f"La reserva #{reserva.id} ya no estaba pendiente.")
    return redirect('reservas:listar_reservas')


def cancelar_reserva(request, pk):
    reserva = get_object_or_404(RegistroReservas, pk=pk)
    if reserva.estado_reserva != 'finalizada':
        reserva.estado_reserva = 'cancelada'
        reserva.save()
        messages.warning(request, f"Reserva #{reserva.id} ha sido cancelada.")
    return redirect('reservas:listar_reservas')


def editar_reserva(request, pk):
    reserva = get_object_or_404(RegistroReservas, pk=pk)

    if request.method == 'POST':
        form = FormularioReservas(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, "Reserva actualizada correctamente.")
            return redirect('reservas:listar_reservas')
        else:
            messages.error(request, "Corrige los errores antes de guardar.")
    else:
        form = FormularioReservas(instance=reserva)

    return render(request, 'Reservas/editar_reserva.html', {'form': form, 'reserva': reserva})


#===================================: Verificar disponibilidad por fechas =====================================================================
def habitaciones_por_tipo_y_fechas(request):
    """
    Retorna habitaciones disponibles según tipo y fechas.
    Considera reservas existentes en esas fechas.
    """
    tipo = request.GET.get('tipo', '').strip().upper()
    fecha_in = request.GET.get('fecha_in', '').strip()
    fecha_out = request.GET.get('fecha_out', '').strip()
    
    habitaciones = []

    if not tipo or not fecha_in or not fecha_out:
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)

    try:
        # Convertir fechas
        fecha_in = datetime.strptime(fecha_in, '%Y-%m-%d').date()
        fecha_out = datetime.strptime(fecha_out, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Formato de fecha inválido'}, status=400)

    # Obtener habitaciones del tipo solicitado
    habitaciones_tipo = Habitacion.objects.filter(tipo=tipo)

    # Filtrar las que tienen reservas conflictivas en esas fechas
    habitaciones_reservadas = RegistroReservas.objects.filter(
        Q(fecha_check_in__lt=fecha_out) & Q(fecha_check_out__gt=fecha_in),
        estado_reserva__in=['pendiente', 'confirmada'],  # Solo activas
        Habitaciones__tipo=tipo
    ).values_list('Habitaciones__id', flat=True)

    # Excluir habitaciones reservadas
    habitaciones_disponibles = habitaciones_tipo.exclude(
        id__in=habitaciones_reservadas
    ).filter(
        estado='DISPONIBLE'  # También debe estar marcada como disponible
    ).values('id', 'numero', 'tipo')

    return JsonResponse(list(habitaciones_disponibles), safe=False)


# ========== Mantener la vista anterior por compatibilidad ==========
def habitaciones_por_tipo(request):
    """Vista simple sin considerar fechas (puedes eliminarla si quieres)"""
    tipo = request.GET.get('tipo', '').strip().upper()
    habitaciones = []

    if tipo:
        habitaciones = Habitacion.objects.filter(
            tipo=tipo,
            estado='DISPONIBLE'
        ).values('id', 'numero', 'tipo')

    return JsonResponse(list(habitaciones), safe=False)