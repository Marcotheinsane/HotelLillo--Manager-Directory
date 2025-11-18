from django.urls import path
from . import views

urlpatterns = [
    path('consultar/', views.consulta_habitaciones, name='consultar_habitaciones'),
    path('registrar/', views.registrar_habitacion, name='registrar_habitacion'),
    path('editar/<int:pk>/', views.editar_habitacion, name='editar_habitacion'),
    path('eliminar/<int:pk>/', views.eliminar_habitacion, name='eliminar_habitacion'),
]
