from django.shortcuts import render, redirect
from .forms import HabitacionForm
from .models import Habitacion
from django.db.models import Q
from django.core.paginator import Paginator


def consulta_habitaciones(request):
    """Vista para consultar y filtrar habitaciones"""
    qs = Habitacion.objects.all().order_by('numero')
    
    # Obtener parámetros de búsqueda
    q = (request.GET.get('q') or '').strip()
    tipo = (request.GET.get('tipo') or '').strip()
    estado = (request.GET.get('estado') or '').strip()
    
    # Aplicar filtro de búsqueda general
    if q:
        num_q = Q()
        if q.isdigit():
            num_q = Q(numero=int(q))
        qs = qs.filter(num_q | Q(tipo__icontains=q) | Q(comodidades__icontains=q))
    
    # Filtro por tipo
    if tipo:
        qs = qs.filter(tipo__icontains=tipo)
    
    # Filtro por estado
    if estado:
        qs = qs.filter(estado=estado)
    
    # Paginación (10 habitaciones por página)
    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    context = {
        'habitaciones': page_obj,
        'page_obj': page_obj,
        'q': q,
        'tipo': tipo,
        'estado': estado,
    }
    return render(request, 'habitacion/consulta.html', context)


def registrar_habitacion(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('consultar_habitaciones')  # Cambiado para redirigir a consulta
    else:
        form = HabitacionForm()
    return render(request, 'habitacion/registrar.html', {'form': form})