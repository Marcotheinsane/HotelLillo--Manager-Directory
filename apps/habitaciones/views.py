from django.shortcuts import render
from .forms import HabitacionForm
from django.shortcuts import redirect
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Habitacion, EstadoHabitacion

def consulta_habitaciones(request):
    qs = Habitacion.objects.all().order_by('numero')

    q = (request.GET.get('q') or '').strip()
    tipo = (request.GET.get('tipo') or '').strip()
    estado = (request.GET.get('estado') or '').strip()

    if q:
        num_q = Q()
        if q.isdigit():
            num_q = Q(numero=int(q))
        qs = qs.filter(num_q | Q(tipo__icontains=q) | Q(comodidades__icontains=q))

    if tipo:
        qs = qs.filter(tipo__icontains=tipo)

    if estado:
        qs = qs.filter(estado=estado)

    paginator = Paginator(qs, 10)  # 10 filas por página
    page_obj = paginator.get_page(request.GET.get('page'))

    ctx = {
        'page_obj': page_obj,
        'q': q,
        'tipo': tipo,
        'estado': estado,
        'EstadoHabitacion': EstadoHabitacion,
    }
    return render(request, 'habitacion/consulta.html', ctx)


def registrar_habitacion(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = HabitacionForm()
<<<<<<< HEAD
    return render(request, 'habitacion/registrar.html', {'form': form})
=======
    return render(request, 'registrar.html', {'form': form})
>>>>>>> 23b9575 (Avance CRUD con función de registro)
