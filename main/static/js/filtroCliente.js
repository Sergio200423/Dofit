document.addEventListener("DOMContentLoaded", function () {
    const filtroForm = document.getElementById("filtro-clientes-form");
    const listaClientes = document.getElementById("lista-clientes");
    const limpiarButton = document.getElementById("limpiar-filtros");

    if (limpiarButton) {
        limpiarButton.addEventListener("click", function () {
            console.log("Botón Limpiar clickeado"); // Depuración

            // Resetear manualmente los campos del formulario
            if (filtroForm) {
                // Limpiar campos de texto
                filtroForm.querySelectorAll("input[type='text']").forEach(input => input.value = "");

                // Desmarcar checkboxes
                filtroForm.querySelectorAll("input[type='checkbox']").forEach(checkbox => checkbox.checked = false);
            }

            // Enviar solicitud para obtener todos los clientes
            fetch("/api/clientes/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken() // Obtener el token CSRF
                },
                body: JSON.stringify({ action: "todos_los_clientes" })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error en la solicitud: ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                console.log("Respuesta del backend al limpiar:", data); // Depuración
                listaClientes.innerHTML = "";

                if (!data.clientes || data.clientes.length === 0) {
                    listaClientes.innerHTML = `<tr><td colspan="7" class="text-center">No se encontraron clientes</td></tr>`;
                    return;
                }

                // Actualizar la tabla con los nuevos datos
                data.clientes.forEach(cliente => {
                    const row = document.createElement("tr");

                    row.innerHTML = `
                        <td>${cliente.id_cliente}</td>
                        <td>
                            <div class="d-flex align-items-center">
                                <div class="ms-3">
                                    <p class="fw-bold mb-1">${cliente.nombre_cliente}</p>
                                </div>
                            </div>
                        </td>
                        <td>${cliente.sexo}</td>
                        <td>${cliente.fecha_nacimiento}</td>
                        <td>
                            ${cliente.membresia ? `<span class="badge badge-success rounded-pill d-inline">${cliente.membresia.nombreMembresia}</span>` : `<span class="badge badge-trashed rounded-pill d-inline">Sin Membresía</span>`}
                        </td>
                        <td>
                            ${cliente.membresia ? (cliente.membresia.estado === "activo" ? `<span class="badge badge-success rounded-pill d-inline">Activo</span>` : `<span class="badge badge-trashed rounded-pill d-inline">Inactivo</span>`) : `<span class="badge badge-trashed rounded-pill d-inline">Inactivo</span>`}
                        </td>
                        <td>
                            <button type="button" class="btn btn-link btn-rounded btn-sm fw-bold">Editar</button>
                        </td>
                    `;

                    listaClientes.appendChild(row);
                });
            })
            .catch(error => {
                console.error("Error al limpiar los filtros:", error);
                listaClientes.innerHTML = `<tr><td colspan="7" class="text-center text-danger">Error al cargar los clientes</td></tr>`;
            });
        });
    }

    // Función para obtener el token CSRF
    function getCSRFToken() {
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]");
        return csrfToken ? csrfToken.value : "";
    }
});