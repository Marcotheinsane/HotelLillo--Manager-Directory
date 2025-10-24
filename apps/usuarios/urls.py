<<<<<<< HEAD
# usuarios/urls.py
from django.urls import path
from . import views

app_name = 'usuarios'
=======
# huesped/urls.py
from django.urls import path
from . import views

app_name = 'huespedes'
>>>>>>> 23b9575 (Avance CRUD con función de registro)

urlpatterns = [
    path('crear/', views.crear_huesped, name='crear_huesped'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
<<<<<<< HEAD
    path('lista/', views.lista_usuarios, name='lista_usuarios'),
    path('eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('registro/', views.registro_usuario, name='registro'),
=======
>>>>>>> 23b9575 (Avance CRUD con función de registro)
]