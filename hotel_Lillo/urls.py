from django.contrib import admin
from django.urls import path, include
from apps.usuarios import views as vi
from apps.reservas import views as vr

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vi.home, name='home'),
    # urls para uso en los templates
    path('Hacer_recervas/', vr.Registrar_reserva, name='Hacer_Reservas'),
    path('cancelar_reserva/<int:reserva_id>/', vr.cancelar_reserva, name='cancelar_reserva'),
    path('lista_reservas/', vr.lista_reservas, name='lista_reservas'),
    # urls de apps
    path('huespedes/', include('apps.usuarios.urls')),
    path('habitacion/', include('apps.habitaciones.urls')),
    path('login/', vi.login_view, name='login'),
    path('logout/', vi.logout_view, name='logout')
]