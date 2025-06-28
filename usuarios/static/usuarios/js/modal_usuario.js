class ModalUsuario {
  constructor() {
    this.modal = document.getElementById("modalUsuario")
    this.form = document.getElementById("usuarioForm")
    this.titulo = document.getElementById("modalUsuarioTitulo")
    this.btnAbrir = document.querySelector(".btn-agregar-usuario")
    this.btnCerrar = document.getElementById("cerrarModal")
    this.btnCancelar = document.getElementById("cancelarModal")
    this.btnGuardar = document.getElementById("guardarUsuario")
    this.overlay = document.querySelector(".modal-overlay")

    this.isEditing = false
    this.currentUserId = null

    this.init()
  }

  init() {
    this.bindEvents()
    this.initPasswordStrength()
    this.initPasswordToggle()
  }

  bindEvents() {
    // Abrir modal
    if (this.btnAbrir) {
      this.btnAbrir.addEventListener("click", () => this.abrirModal())
    }

    // Cerrar modal
    if (this.btnCerrar) {
      this.btnCerrar.addEventListener("click", () => this.cerrarModal())
    }

    if (this.btnCancelar) {
      this.btnCancelar.addEventListener("click", () => this.cerrarModal())
    }

    if (this.overlay) {
      this.overlay.addEventListener("click", () => this.cerrarModal())
    }

    // Cerrar con ESC
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && this.modal.classList.contains("show")) {
        this.cerrarModal()
      }
    })

    // Submit del formulario
    if (this.form) {
      this.form.addEventListener("submit", (e) => this.handleSubmit(e))
    }

    // Validación en tiempo real
    this.initRealTimeValidation()

    // Eliminar usuario (delegación sobre tbody para máxima compatibilidad)
    const tabla = document.getElementById("tablaUsuarios")
    if (tabla) {
      const tbody = tabla.querySelector("tbody") || tabla
      tbody.addEventListener("click", async (e) => {
        if (e.target.classList.contains("btn-eliminar-usuario")) {
          console.log("Botón eliminar detectado", e.target)
          e.preventDefault()
          const row = e.target.closest("tr")
          const usuarioId = row ? row.id.replace("usuario-", "") : null
          if (!usuarioId) return
          if (!confirm("¿Seguro que deseas eliminar este usuario?")) return
          try {
            const response = await fetch("/usuarios/eliminar/", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
              },
              body: JSON.stringify({ usuario_id: usuarioId }),
            })
            const res = await response.json()
            if (res.success) {
              if (row) row.remove()
            } else {
              this.mostrarError(res.error || "No se pudo eliminar el usuario.")
            }
          } catch (err) {
            this.mostrarError("Error de red al eliminar usuario.")
          }
        }
      })
    }
  }

  abrirModal(usuario = null) {
    this.isEditing = !!usuario
    this.currentUserId = usuario ? usuario.id : null

    // Actualizar título
    this.titulo.textContent = this.isEditing ? "Editar Usuario" : "Nuevo Usuario"

    // Actualizar botón
    const btnText = this.btnGuardar.querySelector(".btn-text")
    btnText.textContent = this.isEditing ? "Actualizar Usuario" : "Guardar Usuario"

    // Llenar formulario si es edición
    if (this.isEditing && usuario) {
      this.llenarFormulario(usuario)
    } else {
      this.limpiarFormulario()
    }

    // Mostrar modal
    this.modal.style.display = "block"
    setTimeout(() => {
      this.modal.classList.add("show")
    }, 10)

    // Focus en primer campo
    const primerInput = this.form.querySelector("input")
    if (primerInput) {
      setTimeout(() => primerInput.focus(), 300)
    }

    // Prevenir scroll del body
    document.body.style.overflow = "hidden"
  }

  cerrarModal() {
    this.modal.classList.remove("show")
    setTimeout(() => {
      this.modal.style.display = "none"
      this.limpiarFormulario()
      this.limpiarErrores()
    }, 300)

    // Restaurar scroll del body
    document.body.style.overflow = ""
  }

  llenarFormulario(usuario) {
    document.getElementById("nombre_usuario").value = usuario.nombre_usuario || ""
    document.getElementById("correo").value = usuario.correo || ""
    document.getElementById("rol").value = usuario.rol || ""

    // No llenar la contraseña por seguridad
    const passwordField = document.getElementById("password")
    passwordField.placeholder = "Dejar vacío para mantener contraseña actual"
    passwordField.required = false
  }

  limpiarFormulario() {
    this.form.reset()

    // Restaurar placeholder y required de contraseña
    const passwordField = document.getElementById("password")
    passwordField.placeholder = "Mínimo 8 caracteres"
    passwordField.required = true

    // Limpiar indicador de fuerza de contraseña
    const strengthIndicator = document.getElementById("passwordStrength")
    strengthIndicator.className = "password-strength"
    strengthIndicator.querySelector(".strength-text").textContent = "Ingresa una contraseña"
  }

  limpiarErrores() {
    const errorElements = this.form.querySelectorAll(".form-error")
    errorElements.forEach((error) => {
      error.textContent = ""
    })

    const inputs = this.form.querySelectorAll(".form-input-enhanced, .form-select-enhanced")
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
      // Recopilar datos del formulario manualmente
      const data = {
        nombre_usuario: document.getElementById("nombre_usuario").value.trim(),
        correo: document.getElementById("correo").value.trim(),
        password: document.getElementById("password").value,
        rol: document.getElementById("rol").value,
      }
      const url = this.isEditing ? `/usuarios/editar/${this.currentUserId}/` : "/usuarios/crear/"

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
        this.mostrarExito(res.message || "Usuario guardado correctamente")
        setTimeout(() => {
          this.cerrarModal()
          // Insertar la nueva fila en la tabla de usuarios
          if (res.usuario_html) {
            this.insertarUsuarioEnTabla(res.usuario_html)
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
      console.error("Error:", error)
      this.mostrarError("Error al guardar el usuario. Inténtalo de nuevo.")
    } finally {
      this.mostrarCargando(false)
    }
  }

  insertarUsuarioEnTabla(usuarioHtml) {
    // Busca la tabla de usuarios (ajusta el selector según tu template)
    const tabla = document.getElementById("tablaUsuarios")
    if (tabla) {
      const tbody = tabla.querySelector("tbody") || tabla
      // Inserta la nueva fila al principio
      const temp = document.createElement("tbody")
      temp.innerHTML = usuarioHtml.trim()
      const nuevaFila = temp.firstElementChild
      if (nuevaFila) {
        tbody.insertBefore(nuevaFila, tbody.firstChild)
      }
    }
  }

  validarFormulario() {
    let esValido = true
    this.limpiarErrores()

    // Validar nombre de usuario
    const nombreUsuario = document.getElementById("nombre_usuario").value.trim()
    if (!nombreUsuario) {
      this.mostrarErrorCampo("nombre_usuario", "El nombre de usuario es requerido")
      esValido = false
    } else if (nombreUsuario.length < 3) {
      this.mostrarErrorCampo("nombre_usuario", "El nombre debe tener al menos 3 caracteres")
      esValido = false
    }

    // Validar correo
    const correo = document.getElementById("correo").value.trim()
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!correo) {
      this.mostrarErrorCampo("correo", "El correo electrónico es requerido")
      esValido = false
    } else if (!emailRegex.test(correo)) {
      this.mostrarErrorCampo("correo", "Ingresa un correo electrónico válido")
      esValido = false
    }

    // Validar contraseña (solo si es nuevo usuario o si se ingresó algo)
    const password = document.getElementById("password").value
    if (!this.isEditing && !password) {
      this.mostrarErrorCampo("password", "La contraseña es requerida")
      esValido = false
    } else if (password && password.length < 8) {
      this.mostrarErrorCampo("password", "La contraseña debe tener al menos 8 caracteres")
      esValido = false
    }

    // Validar rol
    const rol = document.getElementById("rol").value
    if (!rol) {
      this.mostrarErrorCampo("rol", "Selecciona un rol")
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
    // Crear notificación de éxito
    const notification = document.createElement("div")
    notification.className = "modal-usuario-notification success"
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
    // Crear notificación de error
    const notification = document.createElement("div")
    notification.className = "modal-usuario-notification error"
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

  initPasswordStrength() {
    const passwordInput = document.getElementById("password")
    const strengthIndicator = document.getElementById("passwordStrength")

    if (!passwordInput || !strengthIndicator) return

    passwordInput.addEventListener("input", (e) => {
      const password = e.target.value
      const strength = this.calculatePasswordStrength(password)

      strengthIndicator.className = `password-strength ${strength.level}`
      strengthIndicator.querySelector(".strength-text").textContent = strength.text
    })
  }

  calculatePasswordStrength(password) {
    if (!password) {
      return { level: "", text: "Ingresa una contraseña" }
    }

    let score = 0

    // Longitud
    if (password.length >= 8) score++
    if (password.length >= 12) score++

    // Caracteres
    if (/[a-z]/.test(password)) score++
    if (/[A-Z]/.test(password)) score++
    if (/[0-9]/.test(password)) score++
    if (/[^A-Za-z0-9]/.test(password)) score++

    if (score < 3) {
      return { level: "weak", text: "Contraseña débil" }
    } else if (score < 4) {
      return { level: "fair", text: "Contraseña regular" }
    } else if (score < 6) {
      return { level: "good", text: "Contraseña buena" }
    } else {
      return { level: "strong", text: "Contraseña fuerte" }
    }
  }

  initPasswordToggle() {
    const toggleBtn = document.getElementById("togglePassword")
    const passwordInput = document.getElementById("password")

    if (!toggleBtn || !passwordInput) return

    toggleBtn.addEventListener("click", () => {
      const isPassword = passwordInput.type === "password"
      passwordInput.type = isPassword ? "text" : "password"

      // Usar id específico para el path del icono
      const icon = document.getElementById("togglePasswordIcon")
      if (icon) {
        if (isPassword) {
          // Icono de ojo cerrado
          icon.setAttribute(
            "d",
            "M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92 1.41-1.41L3.51 1.93 2.1 3.34l2.36 2.36C3.4 6.84 2.25 9.24 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l2.92 2.92 1.41-1.41L12 7z",
          )
        } else {
          // Icono de ojo abierto
          icon.setAttribute(
            "d",
            "M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z",
          )
        }
      }
    })
  }

  initRealTimeValidation() {
    const inputs = this.form.querySelectorAll(".form-input-enhanced, .form-select-enhanced")

    inputs.forEach((input) => {
      input.addEventListener("blur", () => {
        this.validarCampo(input)
      })

      input.addEventListener("input", () => {
        // Limpiar error al escribir
        const errorElement = document.getElementById(`error_${input.name}`)
        if (errorElement && errorElement.textContent) {
          errorElement.textContent = ""
          input.classList.remove("error")
        }
      })
    })
  }

  validarCampo(input) {
    const valor = input.value.trim()
    const nombre = input.name

    switch (nombre) {
      case "nombre_usuario":
        if (!valor) {
          this.mostrarErrorCampo(nombre, "El nombre de usuario es requerido")
        } else if (valor.length < 3) {
          this.mostrarErrorCampo(nombre, "El nombre debe tener al menos 3 caracteres")
        }
        break

      case "correo":
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        if (!valor) {
          this.mostrarErrorCampo(nombre, "El correo electrónico es requerido")
        } else if (!emailRegex.test(valor)) {
          this.mostrarErrorCampo(nombre, "Ingresa un correo electrónico válido")
        }
        break

      case "password":
        if (!this.isEditing && !valor) {
          this.mostrarErrorCampo(nombre, "La contraseña es requerida")
        } else if (valor && valor.length < 8) {
          this.mostrarErrorCampo(nombre, "La contraseña debe tener al menos 8 caracteres")
        }
        break

      case "rol":
        if (!valor) {
          this.mostrarErrorCampo(nombre, "Selecciona un rol")
        }
        break
    }
  }
}

// Estilos para notificaciones del modal de usuario (más específico para evitar conflicto con el navbar)
const notificationStyles = `
.modal-usuario-notification {
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

.modal-usuario-notification.show {
    transform: translateX(0);
}

.modal-usuario-notification.success {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.modal-usuario-notification.error {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

@media (max-width: 768px) {
    .modal-usuario-notification {
        right: 10px;
        left: 10px;
        transform: translateY(-100%);
    }
    .modal-usuario-notification.show {
        transform: translateY(0);
    }
}
`

// Agregar estilos de notificaciones
const styleSheet = document.createElement("style")
styleSheet.textContent = notificationStyles
document.head.appendChild(styleSheet)

// Inicializar cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", () => {
  new ModalUsuario()
})

// Función global para abrir modal en modo edición
window.editarUsuario = (usuario) => {
  const modal = new ModalUsuario()
  modal.abrirModal(usuario)
}
