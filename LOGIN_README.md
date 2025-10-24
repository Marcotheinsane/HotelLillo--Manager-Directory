# Sistema de Login - Hotel Lillo

## Descripción
Se ha implementado un sistema completo de autenticación para el sistema de gestión del Hotel Lillo, utilizando Django y Tailwind CSS para mantener la consistencia visual.

## Características Implementadas

### 1. Autenticación de Usuarios
- Login con validación de credenciales
- Logout seguro
- Redirección automática después del login
- Protección de rutas con `@login_required`

### 2. Interfaz de Usuario
- Template de login responsivo con Tailwind CSS
- Formulario con validación en tiempo real
- Mensajes de error y éxito
- Botón para mostrar/ocultar contraseña
- Efectos visuales y transiciones

### 3. Base de Datos
- Integración con el modelo `User` de Django
- Extensión con `Perfil_empleado` para roles específicos
- Validaciones de formulario personalizadas

## Archivos Modificados/Creados

### Archivos Modificados:
- `apps/usuarios/forms.py` - Agregado LoginForm
- `apps/usuarios/views.py` - Agregadas vistas de login/logout
- `apps/usuarios/urls.py` - Agregadas rutas de autenticación
- `hotel_Lillo/urls.py` - Agregadas rutas principales
- `hotel_Lillo/settings.py` - Configuración de autenticación
- `templates/base.html` - Panel de usuario en navbar

### Archivos Creados:
- `templates/login.html` - Template de login
- `static/js/login.js` - JavaScript para funcionalidades adicionales
- `apps/usuarios/management/commands/create_test_users.py` - Comando para crear usuarios
- `create_users.py` - Script alternativo para crear usuarios

## Usuarios de Prueba

Para crear los usuarios de prueba, ejecuta uno de estos comandos:

### Opción 1: Comando de Django (Recomendado)
```bash
python manage.py create_test_users
```

### Opción 2: Script Python
```bash
python manage.py shell < create_users.py
```

### Usuarios Creados:

**Administrador:**
- Usuario: `admin`
- Contraseña: `admin123`
- Rol: Administrador
- Permisos: Acceso completo al sistema

**Recepcionista:**
- Usuario: `recepcion`
- Contraseña: `recepcion123`
- Rol: Recepcionista
- Permisos: Acceso limitado según configuración

## Configuración de la Base de Datos

El sistema está configurado para usar MySQL con las siguientes credenciales:
- Host: localhost
- Puerto: 3306
- Base de datos: hotel_Lillo
- Usuario: root
- Contraseña: (vacía)

## Uso del Sistema

1. **Acceder al Login:**
   - Visita `http://localhost:8000/login/`
   - O haz clic en "Iniciar Sesión" en la barra de navegación

2. **Iniciar Sesión:**
   - Ingresa las credenciales de uno de los usuarios de prueba
   - El sistema validará las credenciales contra la base de datos

3. **Navegación:**
   - Después del login exitoso, serás redirigido al home
   - La barra de navegación mostrará tu nombre y opción de logout

4. **Cerrar Sesión:**
   - Haz clic en "Cerrar Sesión" en la barra de navegación
   - Serás redirigido al formulario de login

## Seguridad

- Las contraseñas se almacenan con hash seguro
- Protección CSRF en todos los formularios
- Validación de entrada en frontend y backend
- Redirección automática para usuarios no autenticados

## Personalización

Para agregar más usuarios o modificar roles:
1. Accede al panel de administración de Django: `/admin/`
2. O usa el comando `create_test_users` como referencia
3. Modifica el modelo `Perfil_empleado` según necesidades

## Notas Técnicas

- El sistema usa el framework de autenticación nativo de Django
- Los templates están optimizados para dispositivos móviles
- El JavaScript mejora la experiencia de usuario sin ser esencial
- Compatible con la arquitectura SPA existente
