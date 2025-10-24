from django.contrib import admin
from django.urls import path, include
from apps.usuarios import views as vi
from apps.reservas import views as vr

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vi.home, name='home'),
    # urls para uso en los templates
    path('Hacer_recervas/', vr.Registrar_reserva, name='Hacer_Reservas'),
    #ajax
    path('reservas/', include('apps.reservas.urls')),
    path('disponibles/', vr.habitaciones_disponibles, name='habitaciones_disponibles'),
    path('habitaciones_por_tipo/', vr.habitaciones_por_tipo, name='habitaciones_por_tipo'),
    # urls de apps
    path('usuarios/', include('apps.usuarios.urls')),
    path('crear_huesped/', vi.crear_huesped, name='crear_huesped'),
    path('huespedes/', include('apps.usuarios.urls')),
    path('habitacion/', include('apps.habitaciones.urls')),
    path('login/', vi.login_view, name='login'),
    path('logout/', vi.logout_view, name='logout')
]