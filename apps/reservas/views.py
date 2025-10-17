from django.shortcuts import render

# Create your views here.
def Registrar_reserva(request):
    return render(request, 'Reservas/Registro_reservas.html')