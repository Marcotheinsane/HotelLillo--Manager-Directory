from django import forms
from .models import Habitacion

class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ['numero', 'tipo', 'capacidad', 'tarifa', 'comodidades', 'estado']

        widgets = {
            'numero': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl',
                'placeholder': 'Número de habitación'
            }),
            'tipo': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl'
            }),
            'capacidad': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl',
                'placeholder': 'Capacidad máxima'
            }),
            'tarifa': forms.NumberInput(attrs={   # ✅ AQUÍ EL CAMBIO
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl',
                'placeholder': 'Ej: 50000',
                'step': '0.01',  # ✅ Permite decimales si usas DecimalField
            }),
            'comodidades': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl',
                'rows': 3,
                'placeholder': 'WiFi, TV, baño privado...'
            }),
            'estado': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl'
            }),
        }

        labels = {
            'numero': 'Número',
            'tipo': 'Tipo de Habitación',
            'capacidad': 'Capacidad',
            'tarifa': 'Tarifa (CLP)',
            'comodidades': 'Comodidades',
            'estado': 'Estado'
        }
