from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Huesped, Perfil_empleado

class HuespedForm(forms.ModelForm):
    class Meta:
        model = Huesped
        fields = ['nombre', 'apellido', 'tipo_documento', 'numero_documento', 'email', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el apellido'}),
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12345678-9'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56 9 1234 5678'}),
        }

    # ------------------------------------VALIDACIONES BASICAS  -----------------------------------------------------------------------

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre:
            raise forms.ValidationError("El nombre es obligatorio.")
        if len(nombre) < 2:
            raise forms.ValidationError("El nombre debe tener al menos 2 caracteres.")
        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido', '').strip()
        if not apellido:
            raise forms.ValidationError("El apellido es obligatorio.")
        if len(apellido) < 2:
            raise forms.ValidationError("El apellido debe tener al menos 2 caracteres.")
        return apellido

    def clean_numero_documento(self):
        numero = self.cleaned_data.get('numero_documento', '').strip()
        if not numero:
            raise forms.ValidationError("El número de documento es obligatorio.")
        if len(numero) < 5:
            raise forms.ValidationError("El número de documento es demasiado corto.")
        return numero

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if not email:
            raise forms.ValidationError("El correo electrónico es obligatorio.")
        if not "@" in email or "." not in email:
            raise forms.ValidationError("Ingrese un correo electrónico válido.")
        return email

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '').strip()
        if not telefono:
            raise forms.ValidationError("El número de teléfono es obligatorio.")
        if not telefono.replace("+", "").replace(" ", "").isdigit():
            raise forms.ValidationError("El número de teléfono solo debe contener números.")
        if len(telefono) < 8:
            raise forms.ValidationError("El teléfono debe tener al menos 8 dígitos.")
        return telefono

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent',
            'placeholder': 'Nombre de usuario'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent',
            'placeholder': 'Contraseña'
        })
    )

class RegistroEmpleadoForm(UserCreationForm):
    ROLES = (
        ('recepcionista', 'Recepcionista'),
    )
    
    nombre = forms.CharField(
        max_length=40,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent',
            'placeholder': 'Nombre completo'
        })
    )
    rut = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent',
            'placeholder': 'RUT (ej: 12345678-9)'
        })
    )
    rol = forms.ChoiceField(
        choices=ROLES,
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent',
            'placeholder': 'correo@ejemplo.com'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'nombre', 'email', 'rut', 'rol', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent',
                'placeholder': 'Nombre de usuario'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent',
            'placeholder': 'Contraseña'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent',
            'placeholder': 'Confirmar contraseña'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Perfil_empleado.objects.create(
                perfil_empleado=user,
                nombre=self.cleaned_data['nombre'],
                rol=self.cleaned_data['rol'],
                rut=self.cleaned_data['rut']
            )
        return user