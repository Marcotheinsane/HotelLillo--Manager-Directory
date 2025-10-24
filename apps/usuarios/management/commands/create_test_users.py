
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.usuarios.models import Perfil_empleado

class Command(BaseCommand):
    help = 'Crea usuarios de prueba para el sistema de Hotel Lillo'

    def handle(self, *args, **options):
        # Crear usuario administrador
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'Administrador',
                'last_name': 'Hotel Lillo',
                'email': 'admin@hotellillo.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(
                self.style.SUCCESS('✓ Usuario administrador creado: admin / admin123')
            )
        else:
            self.stdout.write(
                self.style.WARNING('✗ Usuario administrador ya existe')
            )
        
        # Crear perfil de empleado para admin
        admin_profile, created = Perfil_empleado.objects.get_or_create(
            perfil_empleado=admin_user,
            defaults={
                'nombre': 'Administrador',
                'rol': 'administrador',
                'rut': '12345678-9'
            }
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS('✓ Perfil de administrador creado')
            )
        else:
            self.stdout.write(
                self.style.WARNING('✗ Perfil de administrador ya existe')
            )
        
        # Crear usuario recepcionista
        recep_user, created = User.objects.get_or_create(
            username='recepcion',
            defaults={
                'first_name': 'María',
                'last_name': 'González',
                'email': 'recepcion@hotellillo.com',
                'is_staff': False,
                'is_superuser': False
            }
        )
        if created:
            recep_user.set_password('recepcion123')
            recep_user.save()
            self.stdout.write(
                self.style.SUCCESS('✓ Usuario recepcionista creado: recepcion / recepcion123')
            )
        else:
            self.stdout.write(
                self.style.WARNING('✗ Usuario recepcionista ya existe')
            )
        
        # Crear perfil de empleado para recepcionista
        recep_profile, created = Perfil_empleado.objects.get_or_create(
            perfil_empleado=recep_user,
            defaults={
                'nombre': 'María González',
                'rol': 'recepcionista',
                'rut': '98765432-1'
            }
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS('✓ Perfil de recepcionista creado')
            )
        else:
            self.stdout.write(
                self.style.WARNING('✗ Perfil de recepcionista ya existe')
            )
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('USUARIOS DE PRUEBA CREADOS:'))
        self.stdout.write('='*50)
        self.stdout.write('Administrador:')
        self.stdout.write('  Usuario: admin')
        self.stdout.write('  Contraseña: admin123')
        self.stdout.write('  Rol: Administrador')
        self.stdout.write('\nRecepcionista:')
        self.stdout.write('  Usuario: recepcion')
        self.stdout.write('  Contraseña: recepcion123')
        self.stdout.write('  Rol: Recepcionista')
        self.stdout.write('='*50)
