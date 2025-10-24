# Hotel-lillo
Características principales:

Sistema de reservas con verificación instantánea de disponibilidad

Módulo de check-in/out con facturación automática

Gestión centralizada de las 32 habitaciones (suites, matrimoniales, twin, familiares)

Control de tarifas por temporada (alta, media, baja)

Registro histórico de huéspedes y preferencias

Gestión de servicios adicionales (llamadas, minibar)

Reportes automáticos de ocupación e ingresos

Roles diferenciados (Administrador/Recepcionista)

Interfaz intuitiva diseñada para reducir tiempos de operación

Objetivos del sistema:

Eliminar dobles reservas y errores de cálculo manual

Reducir tiempo de check-out de 20 a 5 minutos

Optimizar 3-4 horas diarias en gestión telefónica

Mejorar satisfacción del cliente en un 40%

Proporcionar información en tiempo real del estado del hotel

El sistema está desarrollado bajo metodología Scrum y está específicamente diseñado para las necesidades de este hotel familiar, combinando funcionalidad robusta con usabilidad simple para el personal.


# 1 paso para poder correr el programa 
# requisistos tener msql cliente instanlar dependecia esoesifica para django mas sql : pip install "django==4.2.*"
# 2 crear la base de datos en mysql y despues configurar el setings 
# 3 crear migraciones
# 4 correr migraciones

# lunes 20 se implemento formulario de huespedes validaciones en js y implementacion en el template del registro de huespedes 

# jueves 23 se implementa modulo de ingreso de habitaciones, testo pendiente pues no hay forma de acceder sin poder entrar como admin. -Mitsuki

<<<<<<< HEAD
# jueves 23, testeo funcional, se crea un nuevo html y espacio en el navbar para testear el funcionamiento de la insercion <-- Crear una card personalizada y arreglar el forms para que se vea mejor -Mitsuki

# jueves 23, se implementó el sistema de acceso incluyendo login y logout, con la creación de un archivo login.html, tambíen se agregó un registro de nuevos usuarios en la interfaz del login con la creación de dos archivos html: lista_usuarios.html y registro.html. Por último se integró una función de eliminación de usuarios registrados, la cual solo puede cumplir el usuario admin. -Rorro
=======


# jueves 23, testeo funcional, se crea un nuevo html y espacio en el navbar para testear el funcionamiento de la insercion <-- Crear una card personalizada y arreglar el forms para que se vea mejor -Mitsuki



# viernes 24 se finaliza módulo de habitaciones
# Se implementa la visualización de habitaciones con íconos de estado (Disponible 🟢, Ocupada 🔴, Limpieza 🟡, Mantenimiento ⚫).  
# También se agrega el formulario para registrar nuevas habitaciones desde el sistema, con conexión directa a la base de datos.  
# - Validaciones en modelo completadas.  
# - Integración con plantilla base (`base.html`).  
# - Testeo exitoso del registro y visualización.  
# - Próximo paso: agregar filtros dinámicos por tipo y estado. -seba
>>>>>>> 23b9575 (Avance CRUD con función de registro)
