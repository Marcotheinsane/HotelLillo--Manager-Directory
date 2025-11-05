from django import forms
from datetime import date
from .models import RegistroReservas


class FormularioReservas(forms.ModelForm):
    class Meta:
        model = RegistroReservas
        fields = [
            "fecha_check_in",
            "fecha_check_out",
            "Huespedes",
            "Tipo_Habitacion",
            "Habitaciones",
        ]

        widgets = {
            'fecha_check_in': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl '
                         'focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all '
                         'duration-200 hover:border-gray-300',
                'type': 'date'
            }),
            'fecha_check_out': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl '
                         'focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all '
                         'duration-200 hover:border-gray-300',
                'type': 'date'
            }),
            'Huespedes': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl '
                         'focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all '
                         'duration-200 hover:border-gray-300'
            }),
            'Tipo_Habitacion': forms.Select(attrs={     # 👈 Estilo para tipo
                'id': 'id_Tipo_Habitacion',
                'data-url': '/habitaciones_por_tipo/',
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl '
                         'focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all '
                         'duration-200 hover:border-gray-300'
            }),
            'Habitaciones': forms.Select(attrs={        # 👈 Este será filtrado con AJAX
                'id': 'id_Habitaciones',
                'class': 'w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl '
                         'focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all '
                         'duration-200 hover:border-gray-300'
            }),
        }

        labels = {
            'fecha_check_in': 'Check-in',
            'fecha_check_out': 'Check-out',
            'Huespedes': 'Huésped',
            'Tipo_Habitacion': 'Tipo de Habitación',
            'Habitaciones': 'Habitación',
        }

    # --- Validaciones personalizadas ---
    def clean(self):
        cleaned_data = super().clean()
        fecha_in = cleaned_data.get('fecha_check_in')
        fecha_out = cleaned_data.get('fecha_check_out')

        if not fecha_in or not fecha_out:
            raise forms.ValidationError('Debe ingresar ambas fechas.')

        if fecha_out <= fecha_in:
            raise forms.ValidationError('La fecha de salida debe ser posterior a la fecha de entrada.')

        if fecha_in < date.today():
            raise forms.ValidationError('La fecha de entrada no puede ser anterior a hoy.')

        return cleaned_data
