document.addEventListener("DOMContentLoaded", () => {
  console.log("Script registrarEmpleado.js cargado")

  // Elementos del DOM
  const modal = document.getElementById("modalRegistroEmpleados")
  const openModalBtn = document.getElementById("openModalEmpleadoBtn")
  const closeModalBtn = document.querySelector(".close-modal-empleado")
  const cerrarBtn = document.getElementById("cerrarEmpleadoBtn")
  const form = document.getElementById("registroEmpleados")
  const alertMessage = document.getElementById("alert-message-empleado")

  // Funciones para abrir y cerrar el modal
  function openModal() {
    modal.style.display = "block"
    document.body.style.overflow = "hidden"
    modal.removeAttribute("inert")
    establecerFechaRegistroEmpleado()
  }

  function closeModal() {
    modal.style.display = "none"
    document.body.style.overflow = ""
    modal.setAttribute("inert", "")
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
      console.log("Formulario empleado enviado")
      const submitButton = document.querySelector('button[type="submit"]')
      const originalButtonText = submitButton.innerHTML
      submitButton.disabled = true
      submitButton.innerHTML = '<span class="spinner"></span>Procesando...'
      if (alertMessage) alertMessage.style.display = "none"
      const formData = new FormData(form)
      const data = Object.fromEntries(formData.entries())
      console.log("Datos enviados al backend:", data)
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
            actualizarListaEmpleados();
            form.reset()
            establecerFechaRegistroEmpleado()
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
          submitButton.disabled = false
          submitButton.innerHTML = originalButtonText
        })
    })
  }

  // Función para actualizar la lista de empleados
  function actualizarListaEmpleados() {
    fetch("/api/empleados/", {
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
        console.log("Respuesta del servidor: ", data)
        if (data.empleados) {
          const listaEmpleados = document.getElementById("lista-empleados")
          if (!listaEmpleados) {
            console.error("Elemento lista-empleados no encontrado")
            return
          }
          listaEmpleados.innerHTML = ""
          const forloop = { counter: 0 }
          data.empleados.forEach((empleado) => {
            forloop.counter += 1
            const empleadoRow = document.createElement("tr")
            empleadoRow.setAttribute("data-empleado-id", empleado.id_empleado)
            empleadoRow.innerHTML = `
                        <td>${forloop.counter}</td>
                        <td>
                            <div class="d-flex align-items-center">
                                <div class="ms-3">
                                <p class="fw-bold mb-1">${empleado.nombre_empleado}</p>
                                </div>
                            </div>
                        </td>
                        <td>${empleado.turno || ''}</td>
                        <td>${empleado.salario || ''}</td>
                        <td>
                          <a class="btn btn-link btn-rounded btn-sm fw-bold">Editar</a>
                        </td>
                    `
            listaEmpleados.appendChild(empleadoRow)
          })
          if (window.asignarEventosEditarEmpleado) {
            window.asignarEventosEditarEmpleado();
          }
        } else {
          console.error("No se encontraron empleados.")
        }
      })
      .catch((error) => {
        console.error("Error al obtener la lista de empleados:", error)
      })
  }
})

// Función para obtener el token CSRF
function getCSRFToken() {
  const meta = document.querySelector('meta[name="csrf-token"]')
  return meta ? meta.getAttribute("content") : null
}

function establecerFechaRegistroEmpleado() {
    const fechaRegistroInput = document.getElementById("fecha_registro_empleado");
    if (fechaRegistroInput) {
        const hoy = new Date();
        const ano = hoy.getFullYear();
        const mes = String(hoy.getMonth() + 1).padStart(2, "0");
        const dia = String(hoy.getDate()).padStart(2, "0");
        const fechaActual = `${ano}-${mes}-${dia}`;
        fechaRegistroInput.value = fechaActual;
    }
}
