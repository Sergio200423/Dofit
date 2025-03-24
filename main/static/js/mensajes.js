document.addEventListener("DOMContentLoaded", function () {
    // Obtén el nombre de la plantilla actual desde el atributo data-template
    const template = document.body.getAttribute("data-template");

    // Obtén los mensajes desde el atributo data-mensajes
    const mensajesData = document.body.getAttribute("data-mensajes");
    if (mensajesData) {
        // Divide los mensajes usando el separador "|"
        const mensajes = mensajesData.split("|");

        // Define los títulos personalizados según la plantilla
        let titulo = "Mensaje";
        if (template === "iniciosesion") {
            titulo = "¡Inicio de sesión exitoso!";
        }

        // Muestra los mensajes con SweetAlert
        mensajes.forEach((message) => {
            Swal.fire({
                icon: "success",
                title: titulo,
                text: message,
                confirmButtonText: "OK",
            });
        });
    }
});