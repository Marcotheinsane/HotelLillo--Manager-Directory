from django import forms
from .models import Habitacion

class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ['numero', 'tipo', 'capacidad', 'tarifa', 'comodidades', 'estado']
    
    def clean_capacidad(self):
        capacidad = self.cleaned_data['capacidad']
        if capacidad < 1 or capacidad > 10:
            raise forms.ValidationError("La capacidad debe estar entre 1 y 10.")
        return capacidad