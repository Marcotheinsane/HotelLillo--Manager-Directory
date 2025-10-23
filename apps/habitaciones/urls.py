from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_habitacion, name='registrar_habitacion'),
]
