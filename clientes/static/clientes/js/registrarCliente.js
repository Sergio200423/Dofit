document.addEventListener("DOMContentLoaded", () => {

  // Elementos del DOM
  const modal = document.getElementById("modalRegistroClientes")
  const openModalBtn = document.getElementById("openModalBtn")
  const closeModalBtn = document.querySelector(".close-modal")
  const cerrarBtn = document.getElementById("cerrarBtn")
  const form = document.getElementById("registroClientes")
  const alertMessage = document.getElementById("alert-message")

  // Funciones para abrir y cerrar el modal
  function openModal() {
    modal.style.display = "block"
    document.body.style.overflow = "hidden" // Prevenir scroll
    modal.removeAttribute("inert")

    //Establecer la fecha de registro al abrir el modal
    establecerFechaRegistro()
  }

  function closeModal() {
    modal.style.display = "none"
    document.body.style.overflow = "" // Restaurar scroll
    modal.setAttribute("inert", "")
    // Resetear el formulario y los mensajes de alerta
    if (form) form.reset()
    if (alertMessage) alertMessage.style.display = "none"
  }

  // Event listeners para abrir/cerrar el modal
  if (openModalBtn) openModalBtn.addEventListener("click", openModal)
  if (closeModalBtn) closeModalBtn.addEventListener("click", closeModal)
  if (cerrarBtn) cerrarBtn.addEventListener("click", closeModal)

  // Cerrar el modal al hacer clic fuera del contenido
  window.addEventListener("click", (event) => {
    if (event.target === modal) {
      closeModal()
    }
  })

  // Manejo del formulario
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault()

      // Mostrar spinner en el botón de envío
      const submitButton = document.querySelector('button[type="submit"]')
      const originalButtonText = submitButton.innerHTML
      submitButton.disabled = true
      submitButton.innerHTML = '<span class="spinner"></span>Procesando...'

      // Ocultar mensaje de alerta previo
      if (alertMessage) alertMessage.style.display = "none"

      const formData = new FormData(form)
      const data = Object.fromEntries(formData.entries())
      
      fetch(form.action, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify(data),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`)
          }
          return response.json()
        })
        .then((data) => {
          form.setAttribute("data-informacion-aceptada", data.InformacionAceptada)

          if (data.InformacionAceptada) {
            alertMessage.style.display = "block"
            alertMessage.style.backgroundColor = "rgba(16, 185, 129, 0.1)"
            alertMessage.style.color = "var(--success-color)"
            alertMessage.style.border = "1px solid var(--success-color)"
            alertMessage.textContent = data.message

            // Actualizar la lista de clientes y resetear el formulario
            actualizarListaClientes();
            form.reset()
            establecerFechaRegistro() // Establecer la fecha de registro al abrir el modal

          } else {
            alertMessage.style.display = "block"
            alertMessage.style.backgroundColor = "rgba(239, 68, 68, 0.1)"
            alertMessage.style.color = "var(--danger-color)"
            alertMessage.style.border = "1px solid var(--danger-color)"
            alertMessage.textContent = data.message
          }
        })
        .catch((error) => {
          console.error("Error:", error)
          alertMessage.style.display = "block"
          alertMessage.style.backgroundColor = "rgba(239, 68, 68, 0.1)"
          alertMessage.style.color = "var(--danger-color)"
          alertMessage.style.border = "1px solid var(--danger-color)"
          alertMessage.textContent = "Ocurrió un problema al procesar la solicitud. Por favor, inténtalo de nuevo."
        })
        .finally(() => {
          // Restaurar el botón de envío
          submitButton.disabled = false
          submitButton.innerHTML = originalButtonText
        })
    })
  }

  // Función para actualizar la lista de clientes
  function actualizarListaClientes() {
    fetch("/api/clientes/", {
      method: "GET",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then((response) => {
        if (!response.ok) {
          return response.text()
        }
        return response.json()
      })
      .then((data) => {

        if (data.clientes) {
          const listaClientes = document.getElementById("lista-clientes")
          if (!listaClientes) {
            console.error("Elemento lista-clientes no encontrado")
            return
          }

          listaClientes.innerHTML = ""
          const forloop = { counter: 0 }
          data.clientes.forEach((cliente) => {
            forloop.counter += 1
            const membresia = cliente.membresia

            const nombreMembresia = membresia && membresia.nombreMembresia ? membresia.nombreMembresia : "Inactiva"
            const estadoMembresia =
              membresia && membresia.estado ? (membresia.estado === "activo" ? "Activo" : "Inactivo") : "Inactivo"

            const badgeClass =
              membresia && membresia.estado
                ? membresia.estado === "activo"
                  ? "badge-success"
                  : "badge-trashed"
                : "badge-trashed"

            const clienteRow = document.createElement("tr")
            clienteRow.setAttribute("data-cliente-id", cliente.id_cliente)
            clienteRow.innerHTML = `
                        <td>${forloop.counter}</td>
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
                            <span class="badge ${badgeClass} rounded-pill d-inline">
                                ${nombreMembresia}
                            </span>
                        </td>
                        <td>
                            <span class="badge ${badgeClass} rounded-pill d-inline">
                                ${estadoMembresia}
                            </span>
                        </td>
                        <td>
                          <a class="btn btn-link btn-rounded btn-sm fw-bold">Editar</a>
                        </td>
                    `
            listaClientes.appendChild(clienteRow)
          })
          // Llamar a asignarEventosEditar después de actualizar la tabla
          if (window.asignarEventosEditar) {
            window.asignarEventosEditar();
          }
        } else {
          console.error("No se encontraron clientes.")
        }
      })
      .catch((error) => {
        console.error("Error al obtener la lista de clientes:", error)
      })
  }
})

// Función para obtener el token CSRF
function getCSRFToken() {
  const meta = document.querySelector('meta[name="csrf-token"]')
  return meta ? meta.getAttribute("content") : null
}

function establecerFechaRegistro() {
    const fechaRegistroInput = document.getElementById("fecha_registro");
    if (fechaRegistroInput) {
        const hoy = new Date();
        const ano = hoy.getFullYear();
        const mes = String(hoy.getMonth() + 1).padStart(2, "0"); // Meses son 0-indexados
        const dia = String(hoy.getDate()).padStart(2, "0");
        const fechaActual = `${ano}-${mes}-${dia}`;
        fechaRegistroInput.value = fechaActual; // Establece la fecha actual
    }
}