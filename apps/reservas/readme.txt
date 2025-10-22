El modulo de reservas es critico se espera que pueda registrar un usuario, una fecha y hora, y un servicio a reservar. 
Creación automática de nuevo huésped si no existe Consulta de historial de estancias previas

Registro de preferencias para personalizar servicio
en caso de que no exista el huesped, 

Validaciones que se deben Implementar
Solapamiento de fechas

Capacidad máxima de habitación

Integridad de datos del huésped

Consistencia de tarifas según temporada
--------------------------------------------------------

en sintesis el modulo debe poder :

 Seleccionar habitación y fechas disponibles

 Validar que no haya solapamiento de reservas

 Registrar todos los datos del huésped obligatorios

 Generar confirmación automática de reserva

 Manejar tanto huéspedes existentes como nuevos

Flujo de Reserva:

la estructura de datos se ve en models.py
igual que la de habitación y huesped desde sus respectivos modulos