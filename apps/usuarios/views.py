from django.shortcuts import render,redirect
from .models import Perfil_empleado, Huesped
from .models import Huesped
from .forms import HuespedForm
# Create your views here.

def home(request):
    return render(request,'home.html')

def crear_huesped(request):
    if request.method == 'POST':
        form = HuespedForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home.html') 
    
    else:
        form = HuespedForm()
    
    return render(request, 'huesped/Registrar_huesped.html', {'form': form})
