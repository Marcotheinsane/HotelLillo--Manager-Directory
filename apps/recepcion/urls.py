from django.urls import path
from . import views
from .views import seleccionar_huesped, checkout_huesped


app_name = 'recepcion'

urlpatterns = [
    path('seleccionar/', views.seleccionar_huesped, name='seleccionar_huesped'),
    path('checkout/<int:reserva_id>/', views.checkout_huesped, name='checkout_huesped'),
]
