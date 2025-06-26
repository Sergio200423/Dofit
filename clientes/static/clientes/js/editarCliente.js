document.addEventListener("DOMContentLoaded", () => {

  // Elementos del DOM
  const botonesEditar = document.querySelectorAll(".btn.btn-link");
  const modalElement = document.getElementById("modalEditoClientes");
  const form = document.getElementById("editarClienteForm");
  const alertMessage = document.getElementById("alert-message");
  const cerrarBtn = document.getElementById("cerrarBtn");
  const closeModalBtn = document.querySelector(".close-modal")

  // Validar elementos del DOM
  if (!modalElement) {
    console.error("Elementos requeridos no encontrados en el DOM:", {
      modalElement,
      form,
      alertMessage,
    });
    return;
  }

  window.filaSeleccionada = null;
  window.clienteId = null;

  // Funciones para abrir y cerrar el modal (declaradas en el scope global)
  window.openModal = function() {
    const modalElement = document.getElementById("modalEditoClientes");
    if (!modalElement) return;
    modalElement.style.display = "block";
    document.body.style.overflow = "hidden"; // Prevenir scroll
    modalElement.removeAttribute("inert");
  }

  window.closeModal = function() {
    const modalElement = document.getElementById("modalEditoClientes");
    const form = document.getElementById("editarClienteForm");
    const alertMessage = document.getElementById("alert-message");
    if (!modalElement) return;
    modalElement.style.display = "none";
    document.body.style.overflow = ""; // Restaurar scroll
    modalElement.setAttribute("inert", "");
    // Resetear el formulario y los mensajes de alerta
    if (form) form.reset();
    if (alertMessage) alertMessage.style.display = "none";
  }

     if (cerrarBtn) {
    cerrarBtn.addEventListener("click", () => {
        closeModal();
    });
} else {
    console.error("cerrarBtn no encontrado en el DOM.");
}

if (closeModalBtn) {
    closeModalBtn.addEventListener("click", () => {
        closeModal();
    });
} else {
    console.error("closeModalBtn no encontrado en el DOM.");
}

  // Asignar eventos a los botones de "Editar" usando solo la función global
  window.asignarEventosEditar();

  // Cerrar modal al hacer clic fuera
  modalElement.addEventListener("click", (event) => {
    if (event.target.id === "cerrarBtn" || event.target.classList.contains("close-modal")) {
      console.log("Botón de cierre clickeado");
      closeModal();
    }
  });

  // Manejo del formulario
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      console.log("Formulario de edición enviado");

      if (!window.filaSeleccionada || !window.clienteId) {
        console.error("No hay una fila o ID de cliente seleccionado.");
        alertMessage.style.display = "block";
        alertMessage.style.backgroundColor = "rgba(239, 68, 68, 0.1)";
        alertMessage.style.color = "var(--danger-color)";
        alertMessage.style.border = "1px solid var(--danger-color)";
        alertMessage.textContent = "No se seleccionó un cliente para editar.";
        return;
      }

      // Mostrar spinner en el botón de envío
      const submitButton = form.querySelector('button[type="submit"]');
      const originalButtonText = submitButton.innerHTML;
      submitButton.disabled = true;
      submitButton.innerHTML = '<span class="spinner"></span>Procesando...';

      // Ocultar mensaje de alerta previo
      if (alertMessage) alertMessage.style.display = "none";

      const formData = new FormData(form);
      const data = Object.fromEntries(formData.entries());
      data.id = window.clienteId; // Añadir ID al payload

      console.log("Datos enviados al backend:", data);

      fetch(`/clientes/editar_cliente/${window.clienteId}/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify(data),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          form.setAttribute("data-informacion-aceptada", data.InformacionAceptada);

          if (data.InformacionAceptada) {
            alertMessage.style.display = "block";
            alertMessage.style.backgroundColor = "rgba(16, 185, 129, 0.1)";
            alertMessage.style.color = "var(--success-color)";
            alertMessage.style.border = "1px solid var(--success-color)";
            alertMessage.textContent = data.message;

            actualizarListaClientesAjax(); // Actualizar la lista de clientes
            // Cerrar el modal
            closeModal();
          } else {
            alertMessage.style.display = "block";
            alertMessage.style.backgroundColor = "rgba(239, 68, 68, 0.1)";
            alertMessage.style.color = "var(--danger-color)";
            alertMessage.style.border = "1px solid var(--danger-color)";
            alertMessage.textContent = data.message;
          }
        })
        .catch((error) => {
          console.error("Error al actualizar el cliente:", error);
          alertMessage.style.display = "block";
          alertMessage.style.backgroundColor = "rgba(239, 68, 68, 0.1)";
          alertMessage.style.color = "var(--danger-color)";
          alertMessage.style.border = "1px solid var(--danger-color)";
          alertMessage.textContent = "Ocurrió un problema al procesar la solicitud. Por favor, inténtalo de nuevo.";
        })
        .finally(() => {
          // Restaurar el botón de envío
          submitButton.disabled = false;
          submitButton.innerHTML = originalButtonText;
        });
    });
  }
});

// Función para obtener el token CSRF
function getCSRFToken() {
  const meta = document.querySelector('meta[name="csrf-token"]');
  return meta ? meta.getAttribute("content") : null;
}

function actualizarListaClientesAjax() {
  fetch('/api/clientes/', {
    method: "GET",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
  })
    .then(response => response.json())
    .then(data => {
      const tbody = document.getElementById("lista-clientes");
      tbody.innerHTML = ""; // Limpiar la tabla

      data.clientes.forEach((cliente, idx) => {
        const row = document.createElement("tr");
        row.setAttribute("data-cliente-id", cliente.id_cliente);

        row.innerHTML = `
          <td>${idx + 1}</td>
          <td><div class="d-flex align-items-center"><div class="ms-3"><p class="fw-bold mb-1">${cliente.nombre_cliente}</p></div></div></td>
          <td>${cliente.sexo}</td>
          <td>${cliente.fecha_nacimiento}</td>
          <td>
            <span class="badge ${cliente.membresia && cliente.membresia.estado === 'activo' ? 'badge-success' : 'badge-secondary'} rounded-pill d-inline">
              ${cliente.membresia ? cliente.membresia.nombreMembresia : 'Inactiva'}
            </span>
          </td>
          <td>
            <span class="badge ${cliente.membresia && cliente.membresia.estado === 'activo' ? 'badge-success' : 'badge-trashed'} rounded-pill d-inline">
              ${cliente.membresia && cliente.membresia.estado === 'activo' ? 'Activo' : 'Inactivo'}
            </span>
          </td>
          <td>
            <a class="btn btn-link btn-rounded btn-sm fw-bold">Editar</a>
          </td>
        `;
        tbody.appendChild(row);
      });

      // Vuelve a asignar los event listeners a los nuevos botones de editar
      asignarEventosEditar();
    });
}

window.asignarEventosEditar = function() {
  const botonesEditar = document.querySelectorAll(".btn.btn-link");
  const form = document.getElementById("editarClienteForm");
  const alertMessage = document.getElementById("alert-message");
  botonesEditar.forEach((boton, index) => {
    boton.addEventListener("click", () => {
      window.filaSeleccionada = boton.closest("tr");
      if (!window.filaSeleccionada) {
        console.error("No se pudo encontrar la fila asociada al botón.");
        return;
      }
      window.clienteId = window.filaSeleccionada.getAttribute("data-cliente-id");
      if (!window.clienteId) {
        console.error("No se encontró el ID del cliente en la fila.");
        return;
      }
      // Fetch client data
      fetch(`/api/clientes/?cliente_id=${window.clienteId}`, {
        method: "GET",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          // Populate form fields
          form.querySelector("#nombre_cliente").value = data.nombre || "";
          form.querySelector("#sexo").value = data.sexo || "";
          form.querySelector("#fecha_nacimiento").value = data.fecha_nacimiento || "";
          form.querySelector("#membresia").value = data.membresia || "";
          form.querySelector("#fecha_registro").value = data.fecha_registro || "";
          form.querySelector("#carnet_estudiante").value = data.carnet_estudiante || "";
          // Open modal
          openModal();
        })
        .catch((error) => {
          console.error("Error al obtener los datos del cliente:", error);
          alertMessage.style.display = "block";
          alertMessage.style.backgroundColor = "rgba(239, 68, 68, 0.1)";
          alertMessage.style.color = "var(--danger-color)";
          alertMessage.style.border = "1px solid var(--danger-color)";
          alertMessage.textContent = "Error al cargar los datos del cliente.";
        });
    });
  });
}