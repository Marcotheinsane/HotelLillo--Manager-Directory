document.addEventListener("DOMContentLoaded", function () {
    const tipoSelect = document.getElementById("id_Tipo_Habitacion");
    const habitacionesSelect = document.getElementById("id_Habitaciones");

    // Si no existen los campos, no hacemos nada
    if (!tipoSelect || !habitacionesSelect) {
        console.warn("No se encontró el campo de tipo o habitaciones en el formulario.");
        return;
    }

    // Obtenemos la URL desde el atributo data-url del select
    const fetchUrl = tipoSelect.dataset.url;

    tipoSelect.addEventListener("change", function () {
        const tipo = this.value;

        // Limpiar y mostrar estado de carga
        habitacionesSelect.innerHTML = '<option value="">Cargando habitaciones...</option>';

        // Si no hay tipo seleccionado
        if (!tipo) {
            habitacionesSelect.innerHTML = '<option value="">Seleccione un tipo primero</option>';
            return;
        }

        // Llamada AJAX al backend usando la URL de Django
        fetch(`${fetchUrl}?tipo=${tipo}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error HTTP: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // Limpiamos el select de habitaciones
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
                    noOption.textContent = "No hay habitaciones disponibles";
                    noOption.disabled = true;
                    habitacionesSelect.appendChild(noOption);
                }
            })
            .catch(error => {
                console.error("Error al cargar habitaciones:", error);
                habitacionesSelect.innerHTML = '<option value="">Error al cargar habitaciones</option>';
            });
    });
});
