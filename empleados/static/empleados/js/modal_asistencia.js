class ModalAsistencia {
  constructor() {
    this.modal = document.getElementById("modalAsistencia")
    this.form = document.getElementById("asistenciaForm")
    this.titulo = document.getElementById("modalAsistenciaTitulo")
    this.btnAbrir = document.getElementById("registrarAsistenciaBtn")
    this.btnCerrar = document.getElementById("cerrarModalAsistencia")
    this.btnCancelar = document.getElementById("cancelarModalAsistencia")
    this.btnGuardar = document.getElementById("guardarAsistencia")
    this.overlay = document.querySelector(".modal-overlay")

    this.isEditing = false
    this.currentAsistenciaId = null

    this.init()
  }

  init() {
    this.bindEvents()
  }

  bindEvents() {
    if (this.btnAbrir) {
      this.btnAbrir.addEventListener("click", () => this.abrirModal())
    }
    if (this.btnCerrar) {
      this.btnCerrar.addEventListener("click", () => this.cerrarModal())
    }
    if (this.btnCancelar) {
      this.btnCancelar.addEventListener("click", () => this.cerrarModal())
    }
    if (this.overlay) {
      this.overlay.addEventListener("click", () => this.cerrarModal())
    }
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && this.modal.classList.contains("show")) {
        this.cerrarModal()
      }
    })
    if (this.form) {
      this.form.addEventListener("submit", (e) => this.handleSubmit(e))
    }
    // Delegación para editar asistencia
    const tabla = document.getElementById("tablaAsistencias")
    if (tabla) {
      const tbody = tabla.querySelector("tbody") || tabla
      tbody.addEventListener("click", async (e) => {
        if (e.target.classList.contains("btn-eliminar-asistencia")) {
          e.preventDefault()
          const row = e.target.closest("tr")
          const asistenciaId = row ? row.id.replace("asistencia-", "") : null
          if (!asistenciaId) return
          if (!confirm("¿Seguro que deseas eliminar esta asistencia?")) return
          try {
            const response = await fetch("/empleados/asistencia/eliminar/", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
              },
              body: JSON.stringify({ asistencia_id: asistenciaId }),
            })
            const res = await response.json()
            if (res.success) {
              if (row) row.remove()
            } else {
              this.mostrarError(res.error || "No se pudo eliminar la asistencia.")
            }
          } catch (err) {
            this.mostrarError("Error de red al eliminar asistencia.")
          }
        }
        if (e.target.classList.contains("btn-editar-asistencia")) {
          e.preventDefault()
          const row = e.target.closest("tr")
          const asistenciaId = row ? row.id.replace("asistencia-", "") : null
          if (!asistenciaId) return
          // Obtener datos de la fila (puedes mejorarlo con un endpoint AJAX)
          const cells = row.children
          this.abrirModal({
            id: asistenciaId,
            fecha: cells[0].textContent.trim(),
            check_in: cells[1].textContent.trim(),
            check_out: cells[2].textContent.trim(),
            estado: cells[3].textContent.trim(),
          })
        }
      })
    }
  }

  abrirModal(asistencia = null) {
    this.isEditing = !!asistencia
    this.currentAsistenciaId = asistencia ? asistencia.id : null
    this.titulo.textContent = this.isEditing ? "Editar Asistencia" : "Nueva Asistencia"
    const btnText = this.btnGuardar.querySelector(".btn-text")
    btnText.textContent = this.isEditing ? "Actualizar Asistencia" : "Guardar Asistencia"
    if (this.isEditing && asistencia) {
      this.llenarFormulario(asistencia)
    } else {
      this.limpiarFormulario()
    }
    this.modal.style.display = "block"
    setTimeout(() => {
      this.modal.classList.add("show")
    }, 10)
    const primerInput = this.form.querySelector("input, select")
    if (primerInput) {
      setTimeout(() => primerInput.focus(), 300)
    }
    document.body.style.overflow = "hidden"
  }

  cerrarModal() {
    this.modal.classList.remove("show")
    setTimeout(() => {
      this.modal.style.display = "none"
      this.limpiarFormulario()
      this.limpiarErrores()
    }, 300)
    document.body.style.overflow = ""
  }

  llenarFormulario(asistencia) {
    document.getElementById("asistencia_id").value = asistencia.id || ""
    document.getElementById("fecha").value = this.formatFechaInput(asistencia.fecha)
    document.getElementById("check_in").value = asistencia.check_in || ""
    document.getElementById("check_out").value = asistencia.check_out || ""
    document.getElementById("estado").value = asistencia.estado || ""
  }

  limpiarFormulario() {
    this.form.reset()
    document.getElementById("asistencia_id").value = ""
  }

  limpiarErrores() {
    const errorElements = this.form.querySelectorAll(".form-error")
    errorElements.forEach((error) => {
      error.textContent = ""
    })
    const inputs = this.form.querySelectorAll(".form-control, .form-select")
    inputs.forEach((input) => {
      input.classList.remove("error")
    })
  }

  async handleSubmit(e) {
    e.preventDefault()
    if (!this.validarFormulario()) {
      return
    }
    this.mostrarCargando(true)
    try {
      const data = {
        asistencia_id: document.getElementById("asistencia_id").value,
        fecha: document.getElementById("fecha").value,
        check_in: document.getElementById("check_in").value,
        check_out: document.getElementById("check_out").value,
        estado: document.getElementById("estado").value,
      }
      const url = this.isEditing ? `/empleados/asistencia/editar/` : "/empleados/asistencia/crear/"
      const response = await fetch(url, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
        },
      })
      const res = await response.json()
      if (res.success) {
        this.mostrarExito(res.message || "Asistencia guardada correctamente")
        setTimeout(() => {
          this.cerrarModal()
          if (res.asistencia_html) {
            this.insertarAsistenciaEnTabla(res.asistencia_html)
          }
        }, 800)
      } else {
        if (res.errors) {
          this.mostrarErrores(res.errors)
        } else if (res.error) {
          this.mostrarError(res.error)
        }
      }
    } catch (error) {
      this.mostrarError("Error al guardar la asistencia. Inténtalo de nuevo.")
    } finally {
      this.mostrarCargando(false)
    }
  }

  insertarAsistenciaEnTabla(asistenciaHtml) {
    const tabla = document.getElementById("tablaAsistencias")
    if (tabla) {
      const tbody = tabla.querySelector("tbody") || tabla
      const temp = document.createElement("tbody")
      temp.innerHTML = asistenciaHtml.trim()
      const nuevaFila = temp.firstElementChild
      if (nuevaFila) {
        if (this.isEditing) {
          const filaExistente = document.getElementById(`asistencia-${this.currentAsistenciaId}`)
          if (filaExistente) {
            filaExistente.replaceWith(nuevaFila)
            return
          }
        }
        tbody.insertBefore(nuevaFila, tbody.firstChild)
      }
    }
  }

  validarFormulario() {
    let esValido = true
    this.limpiarErrores()
    const fecha = document.getElementById("fecha").value
    if (!fecha) {
      this.mostrarErrorCampo("fecha", "La fecha es requerida")
      esValido = false
    }
    const checkIn = document.getElementById("check_in").value
    if (!checkIn) {
      this.mostrarErrorCampo("check_in", "El check-in es requerido")
      esValido = false
    }
    const estado = document.getElementById("estado").value
    if (!estado) {
      this.mostrarErrorCampo("estado", "Selecciona un estado")
      esValido = false
    }
    return esValido
  }

  mostrarErrorCampo(campo, mensaje) {
    const errorElement = document.getElementById(`error_${campo}`)
    const inputElement = document.getElementById(campo)
    if (errorElement) {
      errorElement.textContent = mensaje
    }
    if (inputElement) {
      inputElement.classList.add("error")
    }
  }

  mostrarErrores(errores) {
    Object.keys(errores).forEach((campo) => {
      this.mostrarErrorCampo(campo, errores[campo])
    })
  }

  mostrarCargando(mostrar) {
    this.btnGuardar.classList.toggle("loading", mostrar)
    this.btnGuardar.disabled = mostrar
    this.btnCancelar.disabled = mostrar
  }

  mostrarExito(mensaje) {
    const notification = document.createElement("div")
    notification.className = "modal-asistencia-notification success"
    notification.innerHTML = `
      <svg width="20" height="20" fill="none" viewBox="0 0 24 24">
        <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z" fill="currentColor"/>
      </svg>
      ${mensaje}
    `
    document.body.appendChild(notification)
    setTimeout(() => {
      notification.classList.add("show")
    }, 100)
    setTimeout(() => {
      notification.remove()
    }, 3000)
  }

  mostrarError(mensaje) {
    const notification = document.createElement("div")
    notification.className = "modal-asistencia-notification error"
    notification.innerHTML = `
      <svg width="20" height="20" fill="none" viewBox="0 0 24 24">
        <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" fill="currentColor"/>
      </svg>
      ${mensaje}
    `
    document.body.appendChild(notification)
    setTimeout(() => {
      notification.classList.add("show")
    }, 100)
    setTimeout(() => {
      notification.remove()
    }, 5000)
  }

  formatFechaInput(fechaStr) {
    // Convierte "28 Jun, 2025" a "2025-06-28" para el input date
    if (!fechaStr) return ""
    const meses = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    const partes = fechaStr.split(" ")
    if (partes.length !== 3) return fechaStr
    const dia = partes[0].padStart(2, "0")
    const mes = (meses.indexOf(partes[1]) + 1).toString().padStart(2, "0")
    const anio = partes[2]
    return `${anio}-${mes}-${dia}`
  }
}

// Estilos para notificaciones del modal de asistencia
const notificationStyles = `
.modal-asistencia-notification {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 16px 20px;
    border-radius: 12px;
    color: white;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 12px;
    z-index: 10000;
    transform: translateX(100%);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}
.modal-asistencia-notification.show {
    transform: translateX(0);
}
.modal-asistencia-notification.success {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}
.modal-asistencia-notification.error {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}
@media (max-width: 768px) {
    .modal-asistencia-notification {
        right: 10px;
        left: 10px;
        transform: translateY(-100%);
    }
    .modal-asistencia-notification.show {
        transform: translateY(0);
    }
}
`
const styleSheet = document.createElement("style")
styleSheet.textContent = notificationStyles
document.head.appendChild(styleSheet)
document.addEventListener("DOMContentLoaded", () => {
  new ModalAsistencia()
})
window.editarAsistencia = (asistencia) => {
  const modal = new ModalAsistencia()
  modal.abrirModal(asistencia)
}
