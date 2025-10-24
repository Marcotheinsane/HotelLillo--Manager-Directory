from django.shortcuts import render
from .forms import HabitacionForm
from django.shortcuts import redirect

def registrar_habitacion(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = HabitacionForm()
    return render(request, 'habitacion/registrar.html', {'form': form})
