# huesped/urls.py
from django.urls import path
from . import views

app_name = 'huespedes'

urlpatterns = [
    path('crear/', views.crear_huesped, name='crear_huesped'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]