from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.contrib import messages
from apps.reservas.models import RegistroReservas

from .forms import FormularioReservas
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

def listar_reservas(request):
    reservas = RegistroReservas.objects.select_related('Huespedes', 'Habitaciones').order_by('-fecha_check_in')
    return render(request, 'Reservas/listar_reservas.html', {'reservas': reservas})


def editar_reserva(request, pk):
    reserva = get_object_or_404(RegistroReservas, pk=pk)

    if request.method == 'POST':
        form = FormularioReservas(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, " Reserva actualizada correctamente.")
            return redirect('reservas:listar_reservas')
        else:
            messages.error(request, " Corrige los errores antes de guardar.")
    else:
        form = FormularioReservas(instance=reserva)

    return render(request, 'Reservas/editar_reserva.html', {'form': form, 'reserva': reserva})


#------------------------------------------------------------------------------------------------------------------------------------
def habitaciones_disponibles(request):
    habitaciones = Habitacion.objects.filter(estado='DISPONIBLE')
    return render(request, 'habitacion/habitaciones_disponibles.html', {'habitaciones': habitaciones})

# metodo para obtener habitaciones por tipo.

def habitaciones_por_tipo(request):
    tipo = request.GET.get('tipo', '').strip().upper()  
    habitaciones = []

    if tipo:
        habitaciones = Habitacion.objects.filter(
            tipo=tipo,
            estado='DISPONIBLE'
        ).values('id', 'numero', 'tipo')

    return JsonResponse(list(habitaciones), safe=False)