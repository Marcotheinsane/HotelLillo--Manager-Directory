from django import forms
from django.forms import formset_factory


class ServiceForm(forms.Form):
    nombre = forms.CharField(
        label='Servicio',
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded'})
    )
    precio = forms.DecimalField(
        label='Precio',
        required=False,
        min_value=0,
        decimal_places=2,
        max_digits=10,
        widget=forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border rounded'})
    )
    cantidad = forms.IntegerField(
        label='Cantidad',
        required=False,
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border rounded'})
    )


# Importante: can_delete=True porque en la plantilla y vista usas form.DELETE
ServiceFormSet = formset_factory(ServiceForm, extra=3, max_num=10, can_delete=True)


class CheckoutForm(forms.Form):
    METODOS = [
        ("efectivo", "Efectivo"),
        ("tarjeta", "Tarjeta"),
        ("transferencia", "Transferencia"),
        ("otro", "Otro"),
    ]

    impuestos = forms.DecimalField(
        label='Impuestos (%)',
        initial=10,
        min_value=0,
        max_value=100,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'w-24 px-2 py-1 border rounded'})
    )
    metodo_pago = forms.ChoiceField(
        label='Método de pago',
        choices=METODOS,
        initial="efectivo",
        widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border rounded'})
    )
    notas = forms.CharField(
        label='Notas',
        required=False,
        widget=forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded', 'rows': 3})
    )
