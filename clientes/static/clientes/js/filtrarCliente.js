document.addEventListener("DOMContentLoaded", function () {
    const filtroForm = document.getElementById("filtro-clientes-form");
    const listaClientes = document.getElementById("lista-clientes");

    if (filtroForm) {
        filtroForm.addEventListener("submit", function (e) {
            e.preventDefault(); // Prevenir el envío automático del formulario

            // Crear un objeto con los datos del formulario
            const formData = new FormData(filtroForm);
            // Permitir acumulación de filtros con el mismo nombre (membresia, sexo, estado)
            const data = {};
            for (const [key, value] of formData.entries()) {
                if (data[key]) {
                    // Si ya existe, convierte a array o agrega al array
                    if (Array.isArray(data[key])) {
                        data[key].push(value);
                    } else {
                        data[key] = [data[key], value];
                    }
                } else {
                    data[key] = value;
                }
            }
            if (data.action) {
                delete data.action;
            }

            // Enviar la solicitud POST al backend a la URL correcta
            cargarEspera(); // Mostrar el mensaje de espera antes de la solicitud
            fetch("/clientes/filtrar_cliente/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken() // Obtener el token CSRF
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error en la solicitud: ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                if (!data.clientes || data.clientes.length === 0) {
                    listaClientes.innerHTML = `<tr><td colspan="7" class="text-center">No se encontraron clientes</td></tr>`;
                    return;
                }
                
                const fragmento = document.createDocumentFragment();
                // Actualizar la tabla con los nuevos datos
                data.clientes.forEach((cliente, idx) => {
                    const row = document.createElement("tr");
                    row.setAttribute("data-cliente-id", cliente.id_cliente);
                    row.innerHTML = `
                        <td>${idx + 1}</td>
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
                            ${cliente.membresia ? `<span class="badge ${cliente.membresia.estado === "activo" ? "badge-success" : "badge-trashed"} rounded-pill d-inline">${cliente.membresia.nombreMembresia}</span>` : `<span class="badge badge-secondary rounded-pill d-inline">Sin Membresía</span>`}
                        </td>
                        <td>
                            ${cliente.membresia ? (cliente.membresia.estado === "activo" ? `<span class="badge badge-success rounded-pill d-inline">Activo</span>` : `<span class="badge badge-trashed rounded-pill d-inline">Inactivo</span>`) : `<span class="badge badge-trashed rounded-pill d-inline">Inactivo</span>`}
                        </td>
                        <td>
                            <a class="btn btn-link btn-rounded btn-sm fw-bold">Editar</a>
                        </td>
                    `;
                    fragmento.appendChild(row);
                });
                listaClientes.innerHTML = "";
                listaClientes.appendChild(fragmento);
                // Reasignar eventos a los botones de editar
                if (window.asignarEventosEditar) {
                    window.asignarEventosEditar();
                }
            })
            .catch(error => {
                console.error("Error al aplicar los filtros:", error);
                listaClientes.innerHTML = `<tr><td colspan="7" class="text-center text-danger">Error al cargar los clientes</td></tr>`;
            });
        });
    }

    // --- Manejo visual de los filtros tipo pill (adaptado del script de la plantilla) ---
    const filtroPills = document.querySelectorAll('.filtro-pill');
    filtroPills.forEach((pill, idx) => {
    });
    const filtrosAplicadosContainer = document.getElementById('filtros-aplicados-container');

    function actualizarFiltrosAplicados() {
      const filtrosAplicados = [];
      filtroPills.forEach((pill, idx) => {
        const checkbox = pill.querySelector('input[type="checkbox"]');
        if (checkbox.checked) {
          filtrosAplicados.push({
            id: checkbox.id,
            value: checkbox.value,
            label: pill.textContent.trim().replace(/\d+/g, '').trim()
          });
        }
      });

      if (filtrosAplicados.length > 0) {
        filtrosAplicadosContainer.style.display = 'flex';
        const etiquetas = filtrosAplicadosContainer.querySelectorAll('.filtro-aplicado');
        etiquetas.forEach(etiqueta => etiqueta.remove());
        filtrosAplicados.forEach(filtro => {
          const etiqueta = document.createElement('div');
          etiqueta.className = 'filtro-aplicado';
          etiqueta.innerHTML = `
            ${filtro.label}
            <i class="fas fa-times" data-filter-id="${filtro.id}"></i>
          `;
          filtrosAplicadosContainer.appendChild(etiqueta);
          const closeIcon = etiqueta.querySelector('i');
          closeIcon.addEventListener('click', function() {
            const filterId = this.getAttribute('data-filter-id');
            const filterCheckbox = document.getElementById(filterId);
            filterCheckbox.checked = false;
            const pillElement = filterCheckbox.closest('.filtro-pill');
            pillElement.classList.remove('active');
            actualizarFiltrosAplicados();
            filtroForm.dispatchEvent(new Event('submit'));
          });
        });
      } else {
        filtrosAplicadosContainer.style.display = 'none';
      }
    }

    filtroPills.forEach(pill => {
      pill.addEventListener('click', function(e) {
        if (e.target.classList.contains('contador')) {
          e.stopPropagation();
          return;
        }
        const checkbox = this.querySelector('input[type="checkbox"]');
        checkbox.checked = !checkbox.checked;
        if (checkbox.checked) {
          this.classList.add('active');
        } else {
          this.classList.remove('active');
        }
        actualizarFiltrosAplicados();
        filtroForm.dispatchEvent(new Event('submit'));
      });
    });

    // Botón para limpiar todos los filtros
    const limpiarFiltrosBtn = document.getElementById('limpiar-filtros');
    if (limpiarFiltrosBtn) {
      limpiarFiltrosBtn.addEventListener('click', function() {
        filtroPills.forEach(pill => {
          const checkbox = pill.querySelector('input[type="checkbox"]');
          checkbox.checked = false;
          pill.classList.remove('active');
        });
        document.getElementById('nombre').value = '';
        actualizarFiltrosAplicados();
        filtroForm.dispatchEvent(new Event('submit'));
      });
    }

    // Inicializar el estado de los filtros al cargar la página
    filtroPills.forEach(pill => {
      const checkbox = pill.querySelector('input[type="checkbox"]');
      if (checkbox.checked) {
        pill.classList.add('active');
      }
    });
    actualizarFiltrosAplicados();

    // --- Buscador en vivo por nombre ---
    const inputNombre = document.getElementById('nombre');
    if (inputNombre) {
      let lastValue = inputNombre.value;
      let debounceTimeout;
      inputNombre.addEventListener('input', function () {
        const value = inputNombre.value;
        if (value === lastValue) return;
        lastValue = value;
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(() => {
          filtroForm.dispatchEvent(new Event('submit'));
        }, 120); // Espera 120ms tras dejar de escribir
      });
    }

    // Función para obtener el token CSRF
    function getCSRFToken() {
        const meta = document.querySelector('meta[name="csrf-token"]');
        return meta ? meta.getAttribute("content") : "";
    }

    // Antes del fetch, muestra loader
function cargarEspera() {
  listaClientes.innerHTML = `<tr><td colspan="7" class="text-center">Cargando...</td></tr>`;
}
});

