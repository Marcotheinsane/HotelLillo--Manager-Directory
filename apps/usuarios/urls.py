# usuarios/urls.py
from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('crear/', views.crear_huesped, name='crear_huesped'),
    # rutas dentro del namespace 'usuarios'
    # listar huéspedes se expone en '/usuarios/huespedes/' (y también hay '/huespedes/' en project urls)
    path('huespedes/', views.listar_huespedes, name='listar_huespedes'),
    path('login/', views.login_view, name='login'),
    # la vista espera 'pk' como nombre del parámetro
    path('editar/<int:pk>/', views.editar_huesped, name='editar_huesped'),
    path('logout/', views.logout_view, name='logout'),
    # lista de usuarios/empleados (administradores)
    path('lista/', views.lista_usuarios, name='lista_usuarios'),
    path('eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('registro/', views.registro_usuario, name='registro'),
    path('historial/<int:pk>/', views.historial_huesped, name='historial_huesped'),
]