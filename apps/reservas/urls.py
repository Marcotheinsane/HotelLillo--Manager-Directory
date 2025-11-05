from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('habitaciones_por_tipo/', views.habitaciones_por_tipo, name='habitaciones_por_tipo'),
    path('habitaciones_por_tipo_y_fechas/', views.habitaciones_por_tipo_y_fechas, name='habitaciones_por_tipo_y_fechas'),
    path('lista/', views.listar_reservas, name='listar_reservas'),
    path('confirmar/<int:pk>/', views.confirmar_reserva, name='confirmar_reserva'),
    path('cancelar/<int:pk>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('editar/<int:pk>/', views.editar_reserva, name='editar_reserva'),
]