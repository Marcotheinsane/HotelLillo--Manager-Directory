from django.contrib import admin
from django.urls import path, include
from apps.usuarios import views as vi
from apps.reservas import views as vr
from .views import home
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    # urls para uso en los templates
    path('Hacer_recervas/', vr.Registrar_reserva, name='Hacer_Reservas'),
    #ajax
    path('reservas/', include('apps.reservas.urls')),
    path('habitaciones_por_tipo/', vr.habitaciones_por_tipo, name='habitaciones_por_tipo'),
    path('habitaciones_por_tipo_y_fechas/', vr.habitaciones_por_tipo_y_fechas, name='habitaciones_por_tipo_y_fechas'),
    # urls de apps
    path('usuarios/', include('apps.usuarios.urls')), 
    path('crear_huesped/', vi.crear_huesped, name='crear_huesped'),
    # `huespedes/` apunta directamente a la vista de listar huéspedes
    # para evitar incluir el mismo módulo de URLs (y su app_name) dos veces
    path('huespedes/', vi.listar_huespedes, name='listar_huespedes'),
    path('habitacion/', include('apps.habitaciones.urls')),
    path('login/', vi.login_view, name='login'),
    path('logout/', vi.logout_view, name='logout'),
    path("recepcion/", include("apps.recepcion.urls")),

    
]