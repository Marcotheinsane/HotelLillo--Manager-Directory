document.addEventListener("DOMContentLoaded", function () {
    const tipoSelect = document.getElementById("id_Tipo_Habitacion");
    const habitacionesSelect = document.getElementById("id_Habitaciones");
    const fechaInInput = document.getElementById("id_fecha_check_in");
    const fechaOutInput = document.getElementById("id_fecha_check_out");

    if (!tipoSelect || !habitacionesSelect || !fechaInInput || !fechaOutInput) {
        console.warn("Faltan elementos del formulario de reservas.");
        return;
    }

    // Función para cargar habitaciones disponibles
    function cargarHabitaciones() {
        const tipo = tipoSelect.value;
        const fechaIn = fechaInInput.value;
        const fechaOut = fechaOutInput.value;

        // Validar que todos los campos necesarios estén completos
        if (!tipo || !fechaIn || !fechaOut) {
            habitacionesSelect.innerHTML = '<option value="">Complete fechas y tipo primero</option>';
            return;
        }

        // Validar que fecha_out > fecha_in
        if (new Date(fechaOut) <= new Date(fechaIn)) {
            habitacionesSelect.innerHTML = '<option value="">Fecha de salida debe ser posterior</option>';
            return;
        }

        // Mostrar estado de carga
        habitacionesSelect.innerHTML = '<option value="">🔄 Verificando disponibilidad...</option>';

        // Llamada AJAX con fechas
        const url = `/habitaciones_por_tipo_y_fechas/?tipo=${tipo}&fecha_in=${fechaIn}&fecha_out=${fechaOut}`;

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error HTTP: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                habitacionesSelect.innerHTML = '<option value="">Seleccione una habitación</option>';

                if (data.length > 0) {
                    data.forEach(habitacion => {
                        const option = document.createElement("option");
                        option.value = habitacion.id;
                        option.textContent = `Habitación ${habitacion.numero} (${habitacion.tipo})`;
                        habitacionesSelect.appendChild(option);
                    });
                } else {
                    const noOption = document.createElement("option");
                    noOption.textContent = "❌ No hay habitaciones disponibles en estas fechas";
                    noOption.disabled = true;
                    habitacionesSelect.appendChild(noOption);
                }
            })
            .catch(error => {
                console.error("Error al cargar habitaciones:", error);
                habitacionesSelect.innerHTML = '<option value="">Error al verificar disponibilidad</option>';
            });
    }

    // Event listeners
    tipoSelect.addEventListener("change", cargarHabitaciones);
    fechaInInput.addEventListener("change", cargarHabitaciones);
    fechaOutInput.addEventListener("change", cargarHabitaciones);
});