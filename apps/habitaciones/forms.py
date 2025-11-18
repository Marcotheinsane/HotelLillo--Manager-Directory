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

    def clean_numero(self):
        numero = self.cleaned_data.get('numero')
        # Asegurarnos que sea positivo y entero
        if numero is None:
            raise forms.ValidationError('El número de habitación es obligatorio.')
        try:
            numero_int = int(numero)
        except (TypeError, ValueError):
            raise forms.ValidationError('El número debe ser numérico.')
        if numero_int <= 0:
            raise forms.ValidationError('El número debe ser mayor que cero.')

        # Control de duplicidad (excluir la instancia actual al editar)
        qs = Habitacion.objects.filter(numero=numero_int)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Ya existe una habitación con ese número.')

        return numero_int

    def clean_comodidades(self):
        comod = self.cleaned_data.get('comodidades') or ''
        if len(comod) > 500:
            raise forms.ValidationError('Comodidades: máximo 500 caracteres.')
        return comod

    def clean_tarifa(self):
        tarifa = self.cleaned_data.get('tarifa')
        if tarifa is None:
            raise forms.ValidationError('La tarifa es obligatoria.')
        try:
            # Django ya convierte a Decimal, pero verificamos valor positivo
            if tarifa <= 0:
                raise forms.ValidationError('La tarifa debe ser mayor que cero.')
        except Exception:
            raise forms.ValidationError('Ingrese una tarifa válida.')
        return tarifa
