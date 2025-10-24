from django.urls import path
from . import views

urlpatterns = [
    path('consultar/', views.consulta_habitaciones, name='consultar_habitaciones'),     
    path('registrar/', views.registrar_habitacion, name='registrar_habitacion'),
]
