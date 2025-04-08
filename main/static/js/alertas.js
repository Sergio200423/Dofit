document.addEventListener("DOMContentLoaded", function () {
    try {
        // Obtener el contenido del elemento <script> con id="mensajes-data"
        const mensajesDataElement = document.getElementById('mensajes-data');
        if (!mensajesDataElement) {
            console.error("No se encontró el elemento con id 'mensajes-data'.");
            return;
        }

        const mensajesData = mensajesDataElement.textContent.trim();
        console.log("Contenido de mensajes-data (antes de parsear):", mensajesData);

        // Intentar parsear el contenido como JSON
        const mensajes = JSON.parse(mensajesData);
        console.log("Mensajes procesados (después de parsear):", mensajes);

        // Iterar sobre los mensajes y mostrarlos con SweetAlert2
        mensajes.forEach(mensaje => {
            Swal.fire({
                icon: mensaje.icono || "info", // Icono por defecto
                title: mensaje.titulo || "Mensaje",
                text: mensaje.texto || "",
                confirmButtonText: mensaje.boton || "OK"
            });
        });
    } catch (error) {
        console.error("Error al procesar los mensajes:", error);
    }
});