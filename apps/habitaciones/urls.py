from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
=======
    path('consultar/', views.consulta_habitaciones, name='consultar_habitaciones'),
>>>>>>> 23b9575 (Avance CRUD con función de registro)
    path('registrar/', views.registrar_habitacion, name='registrar_habitacion'),
]
