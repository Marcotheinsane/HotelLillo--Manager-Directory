from django.urls import path
from . import views

app_name = 'recepcion'

urlpatterns = [
    path('seleccionar/', views.seleccionar_huesped, name='seleccionar_huesped'),
    path('checkout/<int:reserva_id>/', views.checkout_huesped, name='checkout_huesped'),
]
