from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    """Administración simple para usuarios"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'is_active')
    list_filter = ('rol', 'is_active', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información del Hotel', {'fields': ('rol', 'telefono')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Información del Hotel', {'fields': ('rol', 'telefono')}),
    )