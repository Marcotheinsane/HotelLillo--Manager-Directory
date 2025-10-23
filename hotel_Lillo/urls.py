from django.contrib import admin
from django.urls import path, include
from apps.usuarios import views as vi
from apps.reservas import views as vr

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vi.home, name='home'),
    # urls para uso en los templates
    path('Hacer_recervas/', vr.Registrar_reserva, name='Hacer_Reservas'),
    # urls de apps - CORREGIDO
    path('huespedes/', include('apps.usuarios.urls')),
    path('habitaciones/', include('apps.habitaciones.urls')),
]