from django import forms
from datetime import date
from .models import RegistroReservas

class FormularioReservas(forms.ModelForm):

    class Meta:
        model = RegistroReservas
        fields = ["fecha_check_in", "fecha_check_out", "estado_reserva", "Huespedes", 
                  #"numero_habitacion_temporal" 
                ]
        
        #integracion de tailwind en el forms mala practica 
        widgets = {
            'fecha_check_in': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 hover:border-gray-300',
                'type': 'date'
            }),
            'fecha_check_out': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 hover:border-gray-300',
                'type': 'date'
            }),
            'estado_reserva': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 hover:border-gray-300'
            }),
            'Huespedes': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 boarder border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 hover:border-gray-300'
            }),
            'numero_habitacion_temporal': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 hover:border-gray-300',
                'placeholder': 'Ej: 101, 201, 305'
            }),
        }
        labels = {
            'fecha_check_in': 'Check-in',
            'fecha_check_out': 'Check-out',
            'estado_reserva': 'Estado de la Reserva',
            'Huespedes': 'Huésped',
            'numero_habitacion_temporal': 'Número de Habitación',
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_in = cleaned_data.get('fecha_check_in')
        fecha_out = cleaned_data.get('fecha_check_out')
        
        if not fecha_in or not fecha_out:
            raise forms.ValidationError('Debe ingresar ambas fechas')
        
        if fecha_out <= fecha_in:
            raise forms.ValidationError('La fecha de salida debe ser posterior a la fecha de entrada')
        
        if fecha_in < date.today():
            raise forms.ValidationError('La fecha de entrada no puede ser anterior a hoy')
        
        return cleaned_data
    
class FormularioCancelacion(forms.Form):
    """Formulario simple para capturar el motivo de la cancelación."""
    motivo_cancelacion = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}), 
        label='Motivo de la cancelación',
        required=True
    )