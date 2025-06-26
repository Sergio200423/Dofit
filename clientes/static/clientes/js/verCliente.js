document.addEventListener("DOMContentLoaded", function () {
    const filasClientes = document.querySelectorAll("#lista-clientes tr");
    const modalElement = document.getElementById("modalRegistroClientes"); // Reutilizamos el modal existente
    const botonRegistrar = modalElement.querySelector("button[name='submitCliente']"); // Botón "Registrar Cliente"
    const modalTitle = modalElement.querySelector("#modalRegistroClientesLabel"); // Título del modal

    filasClientes.forEach((fila) => {
        fila.addEventListener("click", function (event) {
            // Verificar si el clic ocurrió en la columna de acciones (donde está el botón "Editar")
            if (event.target.closest("button.btn-link")) {
                console.log("Clic en el botón 'Editar', no abrir el modal.");
                return; // Salir sin abrir el modal
            }

            // Extraer los datos del cliente de la fila seleccionada
            const nombreCliente = fila.querySelector("td:nth-child(2) .fw-bold")?.textContent.trim() || "N/A";
            const sexoCliente = fila.querySelector("td:nth-child(3)")?.textContent.trim() || "N/A";
            const fechaNacimiento = fila.querySelector("td:nth-child(4)")?.textContent.trim() || "N/A";
            const membresia = fila.querySelector("td:nth-child(5)")?.textContent.trim() || "N/A";
            const estado = fila.querySelector("td:nth-child(6) .badge")?.textContent.trim() || "N/A";

            // Rellenar los datos en el modal
            document.querySelector("#modalRegistroClientes input[name='nombre']").value = nombreCliente;
            document.querySelector("#modalRegistroClientes select[name='sexo']").value = sexoCliente;
            document.querySelector("#modalRegistroClientes input[name='fecha_nacimiento']").value = fechaNacimiento;
            document.querySelector("#modalRegistroClientes select[name='membresia']").value = membresia;

            // Cambiar el estilo del modal para que sea gris semitransparente
            modalElement.querySelector(".modal-content").style.backgroundColor = "rgba(128, 128, 128, 0.8)";
            modalElement.querySelector(".modal-content").style.color = "white";

            // Cambiar el texto del título del modal
            modalTitle.textContent = "Ver información del Cliente";

            // Ocultar el botón "Registrar Cliente"
            botonRegistrar.style.display = "none";

            // Mostrar el modal
            const modal = new bootstrap.Modal(modalElement);
            modal.show();
        });
    });

    // Restaurar el título y el botón cuando se cierre el modal
    modalElement.addEventListener("hidden.bs.modal", function () {
        botonRegistrar.style.display = ""; // Restaurar el estilo original (mostrar el botón)
        modalElement.querySelector(".modal-content").style.backgroundColor = ""; // Restaurar el color original
        modalElement.querySelector(".modal-content").style.color = ""; // Restaurar el color original
        modalTitle.textContent = "Registrar Cliente"; // Restaurar el título original
    });
});