from django.shortcuts import render
from .models import Perfil_empleado, Huesped
# Create your views here.

def home(request):
    return render(request,'home.html')