// Función para enmascarar el correo electrónico
function maskEmail(email) {
  if (!email) return ""

  const [localPart, domain] = email.split("@")
  if (!domain) return email

  // Mostrar solo los primeros 3-4 caracteres del local part
  const visibleChars = Math.min(4, Math.max(3, localPart.length))
  const maskedLocal = localPart.substring(0, visibleChars) + "*".repeat(Math.max(0, localPart.length - visibleChars))

  return `${maskedLocal}@${domain}`
}

// Función para aplicar el enmascaramiento a todos los correos
function applyEmailMasking() {
  const emailElements = document.querySelectorAll(".user-email[data-email]")

  emailElements.forEach((element) => {
    const originalEmail = element.getAttribute("data-email")
    if (originalEmail) {
      element.textContent = maskEmail(originalEmail)
    }
  })
}

// Función para manejar la selección de usuario
function selectUser(userItem) {
  const checkbox = userItem.querySelector('input[name="correo"]')

  if (!checkbox || checkbox.disabled) return

  // Deseleccionar otros usuarios
  const allUserItems = document.querySelectorAll(".user-item:not(.disabled)")
  const allCheckboxes = document.querySelectorAll('input[name="correo"]:not([disabled])')

  allUserItems.forEach((item) => item.classList.remove("selected"))
  allCheckboxes.forEach((cb) => (cb.checked = false))

  // Seleccionar el usuario actual
  userItem.classList.add("selected")
  checkbox.checked = true

  // Actualizar estado del botón
  updateSubmitButton()
}

// Función para actualizar el estado del botón de envío
function updateSubmitButton() {
  const submitBtn = document.getElementById("btn-enviar")
  const checkedBoxes = document.querySelectorAll('input[name="correo"]:checked')

  submitBtn.disabled = checkedBoxes.length === 0
}

// Función para mostrar el correo completo temporalmente
function showFullEmail(emailElement, originalEmail) {
  if (!originalEmail) return

  const maskedEmail = emailElement.textContent
  emailElement.textContent = originalEmail

  setTimeout(() => {
    emailElement.textContent = maskedEmail
  }, 3000)
}

// Función para manejar el envío del formulario
function handleFormSubmit(event) {
  const submitBtn = document.getElementById("btn-enviar")
  const checkedBox = document.querySelector('input[name="correo"]:checked')

  if (!checkedBox) {
    event.preventDefault()
    alert("Por favor, selecciona un usuario para enviar el correo de recuperación.")
    return
  }

  // Mostrar estado de carga
  submitBtn.classList.add("loading")
  submitBtn.disabled = true

  // El formulario se enviará normalmente a Django
  // Si quieres interceptar y hacer AJAX, descomenta lo siguiente:
  /*
    event.preventDefault();
    
    // Aquí puedes hacer una petición AJAX a tu vista de Django
    fetch(event.target.action, {
        method: 'POST',
        body: new FormData(event.target),
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        // Manejar respuesta
        if (data.success) {
            showSuccessMessage();
            resetForm();
        } else {
            alert('Error al enviar el correo: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al enviar el correo');
    })
    .finally(() => {
        submitBtn.classList.remove('loading');
        updateSubmitButton();
    });
    */
}

// Función para mostrar mensaje de éxito
function showSuccessMessage() {
  const successMessage = document.getElementById("success-message")
  successMessage.style.display = "flex"

  setTimeout(() => {
    successMessage.style.display = "none"
  }, 5000)
}

// Función para resetear el formulario
function resetForm() {
  const userItems = document.querySelectorAll(".user-item.selected")
  const checkboxes = document.querySelectorAll('input[name="correo"]:checked')

  userItems.forEach((item) => item.classList.remove("selected"))
  checkboxes.forEach((checkbox) => (checkbox.checked = false))

  updateSubmitButton()
}

// Inicialización cuando se carga el DOM
document.addEventListener("DOMContentLoaded", () => {
  // Aplicar enmascaramiento de correos
  applyEmailMasking()

  // Configurar el formulario
  const form = document.getElementById("form-correos")
  form.addEventListener("submit", handleFormSubmit)

  // Estado inicial del botón
  updateSubmitButton()

  // Agregar funcionalidad de clic en el item completo
  document.addEventListener("click", (e) => {
    const userItem = e.target.closest(".user-item:not(.disabled)")
    if (userItem) {
      selectUser(userItem)
    }
  })

  // Funcionalidad para mostrar correo completo al hacer doble clic
  document.addEventListener("dblclick", (e) => {
    const userItem = e.target.closest(".user-item:not(.disabled)")
    if (userItem) {
      const emailElement = userItem.querySelector(".user-email[data-email]")
      if (emailElement) {
        const originalEmail = emailElement.getAttribute("data-email")
        showFullEmail(emailElement, originalEmail)
      }
    }
  })

  // Agregar efecto hover mejorado
  const userItems = document.querySelectorAll(".user-item:not(.disabled)")
  userItems.forEach((item, index) => {
    // Aplicar delay de animación basado en el índice
    item.style.animationDelay = `${(index + 1) * 0.1}s`
  })
})

// Función adicional para manejar respuestas del servidor (si usas AJAX)
function handleServerResponse(response) {
  const submitBtn = document.getElementById("btn-enviar")

  if (response.success) {
    showSuccessMessage()
    resetForm()
  } else {
    alert("Error: " + (response.message || "No se pudo enviar el correo"))
  }

  submitBtn.classList.remove("loading")
  updateSubmitButton()
}
