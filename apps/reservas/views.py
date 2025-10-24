from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction 
from .forms import FormularioReservas, FormularioCancelacion 
from .models import RegistroReservas 
from apps.habitaciones.models import Habitacion 

# Create your views here.
def Registrar_reserva(request):
    if request.method == "POST":
        form = FormularioReservas(request.POST)
        if form.is_valid():
            form.save()
            # Redirigir a una página de éxito o mostrar un mensaje
    else:
        form = FormularioReservas()

    return render(request, 'Reservas/Registro_reservas.html', {'form': form})

def lista_reservas(request):
    """
    Muestra todas las reservas activas (pendientes o confirmadas).
    """
    # Excluir las reservas que ya están canceladas (borrado lógico)
    reservas_activas = RegistroReservas.objects.exclude(estado_reserva='cancelada').order_by('fecha_check_in')

    context = {
        'reservas': reservas_activas
    }
    return render(request, 'Reservas/lista_reservas.html', context)

def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(RegistroReservas, pk=reserva_id)

    # Evitar cancelar una reserva que ya está cancelada
    if reserva.estado_reserva == 'cancelada':
        messages.warning(request, f"La reserva #{reserva_id} ya se encuentra cancelada.")
        return redirect('reservas/Registro_reservas.html') # Redirige a donde listes tus reservas

    if request.method == 'POST':
        form = FormularioCancelacion(request.POST)
        if form.is_valid():
            motivo = form.cleaned_data['motivo_cancelacion']
            
            try:
                # 1. INICIO DE TRANSACCIÓN: Asegura que si falla una parte, todo se revierte.
                with transaction.atomic():
                    # A. Borrado Lógico y Registro de Motivo
                    reserva.estado_reserva = 'cancelada'
                    reserva.motivo_cancelacion = motivo
                    reserva.save() 
                    
                    # B. La habitación queda disponible automáticamente
                    habitacion_reservada = reserva.Habitaciones # Objeto Habitacion relacionado
                    
                    habitacion_reservada.estado = 'disponible' 
                    habitacion_reservada.save()
                    
                # 2. FIN DE TRANSACCIÓN EXITOSO
                messages.success(request, f"Reserva #{reserva_id} cancelada con éxito. La habitación {habitacion_reservada.numero_habitacion} está ahora disponible.")
                return redirect('reservas/Registro_reservas.html') # Redirige a la lista de reservas
            
            except Exception as e:
                messages.error(request, f"Ocurrió un error al procesar la cancelación: {e}")
                return redirect('reservas/Registro_reservas.html', reserva_id=reserva_id) 

    else:
        form = FormularioCancelacion()

    context = {
        'reserva': reserva,
        'form': form
    }
    return render(request, 'Reservas/confirmar_cancelacion.html', context)