from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Crea usuarios iniciales para el Hotel Lillo'

    def handle(self, *args, **options):
        self.stdout.write('Creando usuarios iniciales...')
        
        # Crear superusuario si no existe
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@hotellillo.com',
                password='admin123',
                first_name='Administrador',
                last_name='Sistema',
                rol='admin'
            )
            self.stdout.write(
                self.style.SUCCESS('Superusuario creado: admin/admin123')
            )
        
        # Crear usuario recepcionista
        if not User.objects.filter(username='recepcionista').exists():
            User.objects.create_user(
                username='recepcionista',
                email='recepcion@hotellillo.com',
                password='recepcion123',
                first_name='María',
                last_name='González',
                rol='recepcionista'
            )
            self.stdout.write(
                self.style.SUCCESS('Usuario recepcionista creado: recepcionista/recepcion123')
            )
        
        self.stdout.write(
            self.style.SUCCESS('¡Usuarios iniciales creados exitosamente!')
        )
        self.stdout.write('Usuarios de prueba:')
        self.stdout.write('- Administrador: admin/admin123')
        self.stdout.write('- Recepcionista: recepcionista/recepcion123')