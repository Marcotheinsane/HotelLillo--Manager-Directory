from django import forms
from .models import Habitacion


class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ['numero', 'tipo', 'capacidad', 'tarifa', 'comodidades', 'estado']

        widgets = {
            'numero': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl '
                         'focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all '
                         'duration-200 hover:border-gray-300',
                'placeholder': 'Ingrese el número de habitación'
            }),
            'tipo': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl '
                         'focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all '
                         'duration-200 hover:border-gray-300'
            }),
            'capacidad': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl '
                         'focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all '
                         'duration-200 hover:border-gray-300',
                'placeholder': 'Capacidad máxima'
            }),
            'tarifa': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl '
                         'focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all '
                         'duration-200 hover:border-gray-300',
                'placeholder': 'Tarifa por noche'
            }),
            'comodidades': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl '
                         'focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all '
                         'duration-200 hover:border-gray-300',
                'rows': 3,
                'placeholder': 'Ejemplo: Wi-Fi, TV, baño privado...'
            }),
            'estado': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl '
                         'focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all '
                         'duration-200 hover:border-gray-300'
            }),
        }

        labels = {
            'numero': 'Número de Habitación',
            'tipo': 'Tipo de Habitación',
            'capacidad': 'Capacidad (personas)',
            'tarifa': 'Tarifa (CLP)',
            'comodidades': 'Comodidades',
            'estado': 'Estado Actual',
        }
