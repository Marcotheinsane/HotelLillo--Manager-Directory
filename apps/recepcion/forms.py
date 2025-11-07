from django import forms
from django.forms import modelformset_factory
from apps.servicios.models import ServicioConsumido, ServicioCatalogo, Pago

class ServicioConsumidoForm(forms.ModelForm):
    servicio_catalogo = forms.ModelChoiceField(
        queryset=ServicioCatalogo.objects.filter(activo=True).order_by("nombre"),
        required=False,
        label="Servicio",
        widget=forms.Select(attrs={
            'class': 'w-full border rounded px-2 py-1 text-sm'
        })
    )

    class Meta:
        model = ServicioConsumido
        fields = ["servicio_catalogo", "cantidad"]

ServicioFormSet = modelformset_factory(
    ServicioConsumido,
    form=ServicioConsumidoForm,
    extra=3,
    can_delete=True
)


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ["metodo", "notas"]
        widgets = {
            "metodo": forms.Select(attrs={
                'class': 'w-full border rounded px-2 py-1 text-sm'
            }),
            "notas": forms.Textarea(attrs={
                'class': 'w-full border rounded px-2 py-1 text-sm',
                'rows': 3
            })
        }
