from django.shortcuts import render, redirect
from .models import Habitacion
from .forms import HabitacionForm

def registrar_habitacion(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_habitaciones')
    else:
        form = HabitacionForm()
    return render(request, 'habitaciones/registrar.html', {'form': form})

def listar_habitaciones(request):
    habitaciones = Habitacion.objects.all()
    return render(request, 'habitaciones/listar.html', {'habitaciones': habitaciones})