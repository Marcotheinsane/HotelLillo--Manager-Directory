from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .models import Huesped
from apps.reservas.models import RegistroReservas
from django.contrib.auth.models import User
from .models import Perfil_empleado, Huesped
from .forms import HuespedForm, LoginForm, RegistroEmpleadoForm
# Create your views here.
from apps.usuarios.decorators import solo_no_demo


#crud basico de huesedes
@solo_no_demo
def crear_huesped(request):
    if request.method == 'POST':
        form = HuespedForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, 'Huésped registrado correctamente.')
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home') 
    else:
        form = HuespedForm()
    
    return render(request, 'huesped/Registrar_huesped.html', {'form': form})


def listar_huespedes(request):
    huespedes = Huesped.objects.all().order_by('-fecha_registro')

    return render(request, 'huesped/listar_huespedes.html', {'huespedes': huespedes})

@solo_no_demo
def editar_huesped(request, pk):
    huesped = get_object_or_404(Huesped, pk=pk)  # Busca el huésped o lanza 404 si no existe cualquiera de las 2 ocurrre

    if request.method == 'POST':
        form = HuespedForm(request.POST, instance=huesped) #Reutiliza el formulario de django para no repetir codigo
        if form.is_valid():
            form.save()
            messages.success(request, f"Huésped '{huesped.nombre} {huesped.apellido}' actualizado correctamente ")
            return redirect('usuarios:listar_huespedes')
        else:
            messages.error(request, "Corrige los errores antes de guardar.")
    else:
        form = HuespedForm(instance=huesped)  # Precarga los datos existentes 

    return render(request, 'huesped/editar_huesped.html', {'form': form, 'huesped': huesped})

#Aqui se agrega la vista para poder consultar el historial de un huesped
def historial_huesped(request, pk):
    huesped = get_object_or_404(Huesped, pk=pk)
    # Aquí se va agregar la lógica para obtener el historial del huésped
    # Quiero agrupar todos los datos de 1 reserva y su estado si esta actuva o finaliazada ahora si 
    # Tiene mas de una reserva historica se podra vizualizar tambien


# Usuarios- Login y Logout de administradores y empleados

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido, {user.first_name or user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroEmpleadoForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registro exitoso. Por favor, inicia sesión.')
            return redirect('login')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = RegistroEmpleadoForm()
    return render(request, 'usuarios/registro.html', {'form': form})


def historial_huesped(request, pk):
    # Aquí se va agregar la lógica para obtener el historial del huésped
    # Quiero agrupar todos los datos de 1 reserva y su estado si esta actuva o finaliazada ahora si 
    # Tiene mas de una reserva historica se podra vizualizar tambien
    huesped = get_object_or_404(Huesped, pk=pk)
    

    # Obtener todas las reservas del huésped ordenadas por fecha de creación (más reciente primero)
    reservas_historicas = RegistroReservas.objects.filter(
        Huespedes=huesped 
    ).select_related('Habitaciones').order_by('-created_at')
    
    # Clasificar reservas por estado si estan activas o finalizadas
    reservas_activas = reservas_historicas.filter(
        estado_reserva__in=['pendiente', 'confirmada']
    )
    reservas_finalizadas = reservas_historicas.filter(
        estado_reserva__in=['finalizada', 'cancelada']
    )
    
    # Calcular estadísticas del huésped 
    total_reservas = reservas_historicas.count()
    total_gastado = sum(r.pago_estancia for r in reservas_historicas)
    
    context = {
        'huesped': huesped,
        'reservas_historicas': reservas_historicas,
        'reservas_activas': reservas_activas,
        'reservas_finalizadas': reservas_finalizadas,
        'total_reservas': total_reservas,
        'total_gastado': total_gastado,
    }
    return render(request, 'huesped/Historial_huesped.html', context)

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login')


def is_admin(user):
    try:
        return user.perfil_empleado.rol == 'administrador'
    except:
        return False

@login_required
@user_passes_test(is_admin)
def lista_usuarios(request):
    usuarios = User.objects.all().select_related('perfil_empleado')
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})

@login_required
@user_passes_test(is_admin)
def eliminar_usuario(request, user_id):
    if request.method == 'POST':
        usuario = get_object_or_404(User, id=user_id)
        if usuario != request.user:  # Evitar que el admin se elimine a sí mismo
            usuario.delete()
            messages.success(request, 'Usuario eliminado correctamente.')
        else:
            messages.error(request, 'No puedes eliminarte a ti mismo.')
        return redirect('usuarios:lista_usuarios')
    return redirect('usuarios:lista_usuarios')
