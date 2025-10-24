from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('habitaciones_por_tipo/', views.habitaciones_por_tipo, name='habitaciones_por_tipo'),
    path('lista/', views.listar_reservas, name='listar_reservas'),
    path('editar/<int:pk>/', views.editar_reserva, name='editar_reserva'),
]