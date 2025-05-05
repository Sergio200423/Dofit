document.addEventListener("DOMContentLoaded", function () {
    // Selecciona todos los botones de "Editar"
    const botonesEditar = document.querySelectorAll(".btn.btn-link");

    console.log(`Se encontraron ${botonesEditar.length} botones de editar.`); // Depuración

    const modalElement = document.getElementById("modalRegistroClientes");
    if (!modalElement) {
        console.error("El modal 'modalRegistroClientes' no se encontró en el DOM.");
    } else {
        console.log("El modal 'modalRegistroClientes' fue encontrado correctamente.");
    }

    botonesEditar.forEach((boton, index) => {
        boton.addEventListener("click", function () {
            console.log(`Botón de editar clickeado: Botón #${index + 1}`); // Depuración

            // Obtén el cliente seleccionado (fila del botón)
            const fila = boton.closest("tr");
            if (!fila) {
                console.error("No se pudo encontrar la fila asociada al botón.");
                return;
            }

            // Extrae los datos del cliente de la fila
            const nombreCliente = fila.querySelector("td:nth-child(2) .fw-bold")?.textContent.trim() || "N/A";
            const sexoCliente = fila.querySelector("td:nth-child(3)")?.textContent.trim() || "N/A";
            const fechaNacimientoTexto = fila.querySelector("td:nth-child(4)")?.textContent.trim() || "N/A";
            const membresia = fila.querySelector("td:nth-child(5)")?.textContent.trim() || "N/A";

            // Convierte la fecha al formato YYYY-MM-DD
            let fechaNacimiento = "";
            if (fechaNacimientoTexto !== "N/A") {
                const fecha = new Date(fechaNacimientoTexto);
                if (!isNaN(fecha)) {
                    fechaNacimiento = fecha.toISOString().split("T")[0]; // Formato YYYY-MM-DD
                } else {
                    console.error("La fecha de nacimiento no se pudo convertir:", fechaNacimientoTexto);
                }
            }

            console.log("Datos extraídos del cliente:", {
                nombreCliente,
                sexoCliente,
                fechaNacimiento,
                membresia,
            }); // Depuración

            // Rellena los campos del modal con los datos del cliente
            const nombreInput = document.querySelector("#modalRegistroClientes input[name='nombre']");
            const sexoSelect = document.querySelector("#modalRegistroClientes select[name='sexo']");
            const fechaInput = document.querySelector("#modalRegistroClientes input[name='fecha_nacimiento']");
            const membresiaSelect = document.querySelector("#modalRegistroClientes select[name='membresia']");

            if (!nombreInput || !sexoSelect || !fechaInput || !membresiaSelect) {
                console.error("No se encontraron uno o más campos en el modal.");
                return;
            }

            nombreInput.value = nombreCliente;
            sexoSelect.value = sexoCliente;
            fechaInput.value = fechaNacimiento;
            membresiaSelect.value = membresia;

            // Abre el modal
            const modal = new bootstrap.Modal(document.getElementById("modalRegistroClientes"));
            modal.show();
            console.log("Modal abierto con los datos del cliente."); // Depuración
        });
    });
});