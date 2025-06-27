class PasswordValidator {
  constructor() {
    this.password1 = document.getElementById("password1")
    this.password2 = document.getElementById("password2")
    this.submitBtn = document.getElementById("submit-btn")
    this.alertMessage = document.getElementById("alert-message")
    this.alertText = document.getElementById("alert-text")

    this.requirements = {
      length: document.getElementById("length-req"),
      uppercase: document.getElementById("uppercase-req"),
      number: document.getElementById("number-req"),
      symbol: document.getElementById("symbol-req"),
    }

    this.passwordMatch = document.getElementById("password-match")

    this.validationState = {
      length: false,
      uppercase: false,
      number: false,
      symbol: false,
      match: false,
    }

    this.init()
  }

  init() {
    // Reset login attempts
    localStorage.setItem("loginAttempts", "0")

    // Add event listeners
    this.password1.addEventListener("input", () => this.validatePassword1())
    this.password2.addEventListener("input", () => this.validatePassword2())

    // Password toggle functionality
    document.querySelectorAll(".password-toggle").forEach((button) => {
      button.addEventListener("click", (e) => this.togglePassword(e.target.closest(".password-toggle")))
    })

    // Sugerir contraseña segura
    const suggestBtn = document.getElementById("suggest-password-btn")
    const suggestedContainer = document.getElementById("suggested-password-container")
    const suggestedSpan = document.getElementById("suggested-password")
    const copyBtn = document.getElementById("copy-suggested-password")
    if (suggestBtn && suggestedContainer && suggestedSpan && copyBtn) {
      suggestBtn.addEventListener("click", () => {
        const pwd = PasswordUtils.generateSecurePassword(12)
        suggestedSpan.textContent = pwd
        suggestedContainer.style.display = "inline-block"
        // Autocompletar ambos campos
        this.password1.value = pwd
        this.password2.value = pwd
        this.validatePassword1()
        this.validatePassword2()
      })
      copyBtn.addEventListener("click", () => {
        const pwd = suggestedSpan.textContent
        if (pwd) {
          navigator.clipboard.writeText(pwd)
        }
      })
    }

    // Form submission
    document.querySelector(".password-form").addEventListener("submit", (e) => this.handleSubmit(e))
  }

  validatePassword1() {
    const password = this.password1.value

    // Length validation
    this.validationState.length = password.length >= 8
    this.updateRequirement("length", this.validationState.length)

    // Uppercase validation
    this.validationState.uppercase = /[A-Z]/.test(password)
    this.updateRequirement("uppercase", this.validationState.uppercase)

    // Number validation
    this.validationState.number = /\d/.test(password)
    this.updateRequirement("number", this.validationState.number)

    // Symbol validation
    this.validationState.symbol = /[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?~`]/.test(password)
    this.updateRequirement("symbol", this.validationState.symbol)

    // Update input styling
    const allValid = Object.values(this.validationState)
      .slice(0, 4)
      .every((valid) => valid)
    this.password1.classList.toggle("valid", allValid && password.length > 0)
    this.password1.classList.toggle("invalid", !allValid && password.length > 0)

    // Validate password match if password2 has content
    if (this.password2.value) {
      this.validatePassword2()
    }

    this.updateSubmitButton()
  }

  validatePassword2() {
    const password1 = this.password1.value
    const password2 = this.password2.value

    if (password2.length === 0) {
      this.passwordMatch.classList.remove("show", "valid")
      this.validationState.match = false
      this.password2.classList.remove("valid", "invalid")
    } else {
      this.passwordMatch.classList.add("show")
      this.validationState.match = password1 === password2 && password1.length > 0

      this.passwordMatch.classList.toggle("valid", this.validationState.match)
      this.password2.classList.toggle("valid", this.validationState.match)
      this.password2.classList.toggle("invalid", !this.validationState.match)

      // Update match indicator
      const icon = this.passwordMatch.querySelector("i")
      const text = this.passwordMatch.querySelector("span")

      if (this.validationState.match) {
        icon.className = "fas fa-check"
        text.textContent = "Las contraseñas coinciden"
      } else {
        icon.className = "fas fa-times"
        text.textContent = "Las contraseñas deben coincidir"
      }
    }

    this.updateSubmitButton()
  }

  updateRequirement(type, isValid) {
    const requirement = this.requirements[type]
    if (requirement) {
      requirement.classList.toggle("valid", isValid)
      const icon = requirement.querySelector("i")
      icon.className = isValid ? "fas fa-check" : "fas fa-times"
    }
  }

  updateSubmitButton() {
    const allValid = Object.values(this.validationState).every((valid) => valid)
    this.submitBtn.disabled = !allValid
  }

  togglePassword(button) {
    const targetId = button.getAttribute("data-target")
    const input = document.getElementById(targetId)
    const icon = button.querySelector("i")

    if (input.type === "password") {
      input.type = "text"
      icon.classList.remove("fa-eye-slash")
      icon.classList.add("fa-eye")
      button.setAttribute("aria-label", "Ocultar contraseña")
    } else {
      input.type = "password"
      icon.classList.remove("fa-eye")
      icon.classList.add("fa-eye-slash")
      button.setAttribute("aria-label", "Mostrar contraseña")
    }
  }

  showAlert(message, type = "error") {
    this.alertText.textContent = message
    this.alertMessage.className = `alert-message ${type}`
    this.alertMessage.classList.remove("hidden")

    // Auto-hide after 5 seconds
    setTimeout(() => {
      this.hideAlert()
    }, 5000)
  }

  hideAlert() {
    this.alertMessage.classList.add("hidden")
  }

  handleSubmit(e) {
    // Final validation
    const allValid = Object.values(this.validationState).every((valid) => valid)

    if (!allValid) {
      e.preventDefault()
      this.showAlert("Por favor, completa todos los requisitos de la contraseña.", "error")
      return
    }

    // Check if passwords are the same as current (simulate)
    const newPassword = this.password1.value

    // Simulate checking against current password
    // In real implementation, this would be done server-side
    if (this.isPasswordSameAsCurrent(newPassword)) {
      e.preventDefault()
      this.showAlert("La nueva contraseña no puede ser igual a la actual.", "error")
      return
    }

    // Si todo es válido, permitir el envío al backend (NO preventDefault)
    // El backend se encargará de mostrar el mensaje de éxito y limpiar el formulario
  }

  isPasswordSameAsCurrent(newPassword) {
    // This is a simulation - in real app, this check would be done server-side
    // For demo purposes, let's say "password123" is the current password
    const currentPassword = "password123"
    return newPassword === currentPassword
  }

  resetForm() {
    document.querySelector(".password-form").reset()
    this.validationState = {
      length: false,
      uppercase: false,
      number: false,
      symbol: false,
      match: false,
    }

    // Reset UI states
    Object.values(this.requirements).forEach((req) => req.classList.remove("valid"))
    this.passwordMatch.classList.remove("show", "valid")
    this.password1.classList.remove("valid", "invalid")
    this.password2.classList.remove("valid", "invalid")
    this.updateSubmitButton()
    this.hideAlert()
  }

  // Utility method for password strength assessment
  getPasswordStrength(password) {
    let strength = 0

    if (password.length >= 8) strength++
    if (/[a-z]/.test(password)) strength++
    if (/[A-Z]/.test(password)) strength++
    if (/\d/.test(password)) strength++
    if (/[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?~`]/.test(password)) strength++
    if (password.length >= 12) strength++

    const strengthLevels = ["Muy débil", "Débil", "Regular", "Buena", "Fuerte", "Muy fuerte"]
    return {
      score: strength,
      level: strengthLevels[Math.min(strength, strengthLevels.length - 1)],
    }
  }
}

// Initialize when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  new PasswordValidator()
})

// Additional utility functions
const PasswordUtils = {
  // Generate a secure password suggestion
  generateSecurePassword(length = 12) {
    const lowercase = "abcdefghijklmnopqrstuvwxyz"
    const uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    const numbers = "0123456789"
    const symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    let password = ""

    // Ensure at least one character from each category
    password += lowercase[Math.floor(Math.random() * lowercase.length)]
    password += uppercase[Math.floor(Math.random() * uppercase.length)]
    password += numbers[Math.floor(Math.random() * numbers.length)]
    password += symbols[Math.floor(Math.random() * symbols.length)]

    // Fill the rest randomly
    const allChars = lowercase + uppercase + numbers + symbols
    for (let i = password.length; i < length; i++) {
      password += allChars[Math.floor(Math.random() * allChars.length)]
    }

    // Shuffle the password
    return password
      .split("")
      .sort(() => Math.random() - 0.5)
      .join("")
  },
}
