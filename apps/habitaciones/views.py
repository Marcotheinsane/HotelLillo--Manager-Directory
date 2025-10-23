from django.shortcuts import render, redirect
from .models import Habitacion
from .forms import HabitacionForm

def registrar_habitacion(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = HabitacionForm()
    return render(request, 'registrar.html', {'form': form})
