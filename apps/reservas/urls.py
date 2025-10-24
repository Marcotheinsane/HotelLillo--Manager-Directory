from django.urls import path
from . import views

urlpatterns = [
    path('cancelar/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('lista/', views.lista_reservas, name='lista_reservas'),  
]