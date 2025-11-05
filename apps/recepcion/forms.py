from django import forms
from django.forms import formset_factory


class ServiceForm(forms.Form):
    nombre = forms.CharField(label='Servicio', max_length=100, required=False,
                             widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded'}))
    precio = forms.DecimalField(label='Precio', required=False, min_value=0, decimal_places=2,
                               widget=forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border rounded'}))


ServiceFormSet = formset_factory(ServiceForm, extra=1, max_num=10)


class CheckoutForm(forms.Form):
    impuestos = forms.DecimalField(label='Impuestos (%)', initial=10, min_value=0, max_value=100,
                                   decimal_places=2, widget=forms.NumberInput(attrs={'class': 'w-24 px-2 py-1 border rounded'}))
    notas = forms.CharField(label='Notas', required=False,
                            widget=forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded', 'rows':3}))
