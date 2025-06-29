class ModalAsistencia {
  constructor() {
    this.modal = document.getElementById("modalAsistencia")
    this.form = document.getElementById("asistenciaForm")
    this.titulo = document.getElementById("modalAsistenciaTitulo")
    this.btnAbrir = document.getElementById("registrarAsistenciaBtn")
    this.btnCerrar = document.getElementById("cerrarModalAsistencia")
    this.btnCancelar = document.getElementById("cancelarModalAsistencia")
    this.btnGuardar = document.getElementById("guardarAsistencia")

    this.isEditing = false
    this.currentAsistenciaId = null

    this.init()
  }

  init() {
    this.bindEvents()
  }

  bindEvents() {
    // Abrir modal
    if (this.btnAbrir) {
      this.btnAbrir.addEventListener("click", (e) => {
        e.preventDefault()
        this.abrirModal()
      })
    }

    // Cerrar modal
    if (this.btnCerrar) {
      this.btnCerrar.addEventListener("click", (e) => {
        e.preventDefault()
        this.cerrarModal()
      })
    }

    if (this.btnCancelar) {
      this.btnCancelar.addEventListener("click", (e) => {
        e.preventDefault()
        this.cerrarModal()
      })
    }

    // Cerrar modal solo al hacer clic en el overlay (fondo), no en el contenido
    if (this.modal) {
      this.modal.addEventListener("click", (e) => {
        // Solo cerrar si el clic fue directamente en el overlay, no en sus hijos
        if (e.target === this.modal) {
          this.cerrarModal()
        }
      })
    }

    // Prevenir que clics en el contenido del modal se propaguen al overlay
    const modalContent = this.modal?.querySelector(".modal-content")
    if (modalContent) {
      modalContent.addEventListener("click", (e) => {
        e.stopPropagation()
      })
    }

    // Cerrar con Escape
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && this.modal?.style.display === "block") {
        this.cerrarModal()
      }
    })

    // Submit del formulario
    if (this.form) {
      this.form.addEventListener("submit", (e) => this.handleSubmit(e))
    }

    // Delegación para editar/eliminar asistencia
    const tabla = document.getElementById("tablaAsistencias")
    if (tabla) {
      tabla.addEventListener("click", (e) => {
        if (e.target.closest(".btn-eliminar-asistencia")) {
          e.preventDefault()
          this.handleEliminar(e.target.closest(".btn-eliminar-asistencia"))
        }

        if (e.target.closest(".btn-editar-asistencia")) {
          e.preventDefault()
          this.handleEditar(e.target.closest(".btn-editar-asistencia"))
        }
      })
    }
  }

  abrirModal(asistencia = null) {
    this.isEditing = !!asistencia
    this.currentAsistenciaId = asistencia ? asistencia.id : null

    this.titulo.textContent = this.isEditing ? "Editar Asistencia" : "Nueva Asistencia"

    const btnText = this.btnGuardar.querySelector(".btn-text")
    if (btnText) {
      btnText.innerHTML = this.isEditing
        ? '<i class="fas fa-save"></i> Actualizar Asistencia'
        : '<i class="fas fa-save"></i> Guardar Asistencia'
    }

    if (this.isEditing && asistencia) {
      this.llenarFormulario(asistencia)
    } else {
      this.limpiarFormulario()
    }

    this.modal.style.display = "block"
    setTimeout(() => {
      this.modal.classList.add("show")
    }, 10)

    // Focus en el primer input
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
    const inputs = this.form.querySelectorAll(".form-control")
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

      // Simular llamada a API (reemplazar con tu endpoint real)
      await new Promise((resolve) => setTimeout(resolve, 1000))

      this.mostrarExito("Asistencia guardada correctamente")
      setTimeout(() => {
        this.cerrarModal()
        // Aquí podrías actualizar la tabla
      }, 800)
    } catch (error) {
      this.mostrarError("Error al guardar la asistencia. Inténtalo de nuevo.")
    } finally {
      this.mostrarCargando(false)
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

  mostrarCargando(mostrar) {
    if (this.btnGuardar) {
      this.btnGuardar.disabled = mostrar
      const spinner = this.btnGuardar.querySelector(".btn-spinner")
      if (spinner) {
        spinner.style.display = mostrar ? "inline-block" : "none"
      }
    }
    if (this.btnCancelar) {
      this.btnCancelar.disabled = mostrar
    }
  }

  mostrarExito(mensaje) {
    this.mostrarNotificacion(mensaje, "success")
  }

  mostrarError(mensaje) {
    this.mostrarNotificacion(mensaje, "error")
  }

  mostrarNotificacion(mensaje, tipo) {
    const toastContainer = document.getElementById("toastContainer")
    if (!toastContainer) return

    const toast = document.createElement("div")
    toast.className = `toast ${tipo}`

    const icon =
      tipo === "success" ? '<i class="fas fa-check-circle"></i>' : '<i class="fas fa-exclamation-circle"></i>'

    toast.innerHTML = `${icon} ${mensaje}`

    toastContainer.appendChild(toast)

    setTimeout(() => toast.classList.add("show"), 100)
    setTimeout(() => {
      toast.classList.remove("show")
      setTimeout(() => toast.remove(), 300)
    }, 4000)
  }

  formatFechaInput(fechaStr) {
    if (!fechaStr) return ""
    // Convertir formato de fecha si es necesario
    return fechaStr
  }

  handleEliminar(btn) {
    const row = btn.closest("tr")
    const asistenciaId = row?.id?.replace("asistencia-", "")

    if (!asistenciaId || !confirm("¿Seguro que deseas eliminar esta asistencia?")) {
      return
    }

    // Simular eliminación
    console.log("Eliminando asistencia:", asistenciaId)
    row.remove()
    this.mostrarExito("Asistencia eliminada correctamente")
  }

  handleEditar(btn) {
    const row = btn.closest("tr")
    const asistenciaId = row?.id?.replace("asistencia-", "")

    if (!asistenciaId) return

    // Obtener datos de la fila para editar
    const cells = row.children
    const asistencia = {
      id: asistenciaId,
      fecha: cells[0]?.textContent?.trim() || "",
      check_in: cells[1]?.textContent?.trim() || "",
      check_out: cells[2]?.textContent?.trim() || "",
      estado: cells[4]?.textContent?.trim() || "",
    }

    this.abrirModal(asistencia)
  }
}

// Inicializar cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", () => {
  window.modalAsistencia = new ModalAsistencia()
})
