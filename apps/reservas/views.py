from django.shortcuts import render
from .forms import FormularioReservas
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