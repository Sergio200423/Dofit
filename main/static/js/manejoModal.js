document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById('registroCliente');
    var alertMessage = document.getElementById('alert-message');
    var modalElement = document.getElementById('testModal'); // Asegúrate de que el ID del modal sea correcto

    if (modalElement) {
        // Escuchar el evento 'show.bs.modal' para limpiar el mensaje de alerta al abrir el modal
        modalElement.addEventListener('show.bs.modal', function () {
            if (alertMessage) {
                alertMessage.style.display = 'none'; // Ocultar el mensaje de alerta
                alertMessage.textContent = ''; // Limpiar el contenido del mensaje
            }
        });
    }

    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault(); // Evitar el envío normal del formulario

            var formData = new FormData(form);
            var submitButton = document.getElementById('submitCliente');

            // Deshabilitar el botón para evitar múltiples envíos
            submitButton.disabled = true;

            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Indicar que es una solicitud AJAX
                }
            })
            .then(response => response.json())
            .then(data => {
                // Actualizar el atributo data-informacion-aceptada
                form.setAttribute('data-informacion-aceptada', data.InformacionAceptada);
                console.log("data.InformacionAceptada: " + data.InformacionAceptada); // Depuración
                if (data.InformacionAceptada) {
                    // Mostrar el mensaje de éxito dentro del modal
                    alertMessage.style.display = 'block';
                    alertMessage.style.color = 'green'; // Cambiar el color a verde
                    alertMessage.textContent = data.message;

                    actualizarListaClientes(); // Recargar la lista de clientes
                    form.reset(); // Limpiar el formulario
                } else {
                    // Mostrar el mensaje de error dentro del modal
                    alertMessage.style.display = 'block';
                    alertMessage.style.color = 'red'; // Cambiar el color a rojo
                    alertMessage.textContent = data.message;

                    console.log("Error en la validación: " + data.message); // Depuración
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alertMessage.style.display = 'block';
                alertMessage.style.color = 'red'; // Cambiar el color a rojo
                alertMessage.textContent = "Ocurrió un problema al procesar la solicitud. Por favor, inténtalo de nuevo.";
            })
            .finally(() => {
                submitButton.disabled = false; // Rehabilitar el botón
            });
        });
    } else {
        console.error("Formulario no encontrado"); // Depuración
    }
});


