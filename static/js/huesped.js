// huespedes.js - Función para abrir popup de huéspedes en nueva ventana
console.log("JS de huésped cargado correctamente");


function abrirPopupHuesped() {
    const width = 600;
    const height = 700;
    const left = (screen.width - width) / 2;
    const top = (screen.height - height) / 2;

    //URL para poder llamarlo desde el formulario y del popup 
    const url = '/huespedes/crear/';

    const popup = window.open(
        url,
        "nuevoHuesped",
        `width=${width},height=${height},left=${left},top=${top},resizable=yes,scrollbars=yes`
    );

    // logica: validacion PARA poder ver si se renderizo la pagina correctamente
    if (popup) {
        const checkClosed = setInterval(function () {
            if (popup.closed) {
                clearInterval(checkClosed);
                location.reload(); // Recarga la página cuando se cierra el popup
            }
        }, 500);
    } else {
        alert('Por favor permite ventanas emergentes para esta página');
    }
}
