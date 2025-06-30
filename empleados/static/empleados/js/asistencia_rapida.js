class AsistenciaRapida {
  constructor() {
    this.currentStatus = "AUSENTE"
    this.checkInTime = null
    this.checkOutTime = null
    this.isLoading = false

    this.elements = {
      currentTime: document.getElementById("currentTime"),
      currentDate: document.getElementById("currentDate"),
      employeeStatus: document.getElementById("employeeStatus"),
      currentStatus: document.getElementById("currentStatus"),
      timeInfo: document.getElementById("timeInfo"),
      entryTime: document.getElementById("entryTime"),
      exitTime: document.getElementById("exitTime"),
      checkInTime: document.getElementById("checkInTime"),
      checkOutTime: document.getElementById("checkOutTime"),
      quickCheckInBtn: document.getElementById("quickCheckInBtn"),
      quickCheckOutBtn: document.getElementById("quickCheckOutBtn"),
      completedStatus: document.getElementById("completedStatus"),
      workedHours: document.getElementById("workedHours"),
      todayCheckIn: document.getElementById("todayCheckIn"),
      todayCheckOut: document.getElementById("todayCheckOut"),
      todayHours: document.getElementById("todayHours"),
      todayStatus: document.getElementById("todayStatus"),
    }

    this.init()
  }

  init() {
    this.updateClock()
    this.bindEvents()
    this.loadTodayAttendance()

    // Actualizar reloj cada segundo
    setInterval(() => this.updateClock(), 1000)
  }

  bindEvents() {
    if (this.elements.quickCheckInBtn) {
      this.elements.quickCheckInBtn.addEventListener("click", () => this.handleQuickCheckIn())
    }

    if (this.elements.quickCheckOutBtn) {
      this.elements.quickCheckOutBtn.addEventListener("click", () => this.handleQuickCheckOut())
    }
  }

  updateClock() {
    const now = new Date()

    if (this.elements.currentTime) {
      this.elements.currentTime.textContent = now.toLocaleTimeString("es-ES", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      })
    }

    if (this.elements.currentDate) {
      this.elements.currentDate.textContent = now.toLocaleDateString("es-ES", {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
      })
    }
  }

  async handleQuickCheckIn() {
    if (this.isLoading || this.currentStatus !== "AUSENTE") return

    this.setLoading(true)
    this.showToast("Marcando entrada...", "info")

    try {
      const now = new Date()
      const timeString = now.toLocaleTimeString("es-ES", {
        hour: "2-digit",
        minute: "2-digit",
      })

      // Simular llamada a API
      const response = await this.makeApiCall("/empleados/asistencia/checkin/", {
        fecha: now.toISOString().split("T")[0],
        check_in: timeString,
        estado: "EN_CURSO",
      })

      if (response.success) {
        this.checkInTime = timeString
        this.updateStatus("EN_CURSO")
        this.updateUI()
        this.showToast("¡Entrada marcada correctamente!", "success")
      } else {
        throw new Error(response.error || "Error al marcar entrada")
      }
    } catch (error) {
      this.showToast("Error al marcar entrada: " + error.message, "error")
    } finally {
      this.setLoading(false)
    }
  }

  async handleQuickCheckOut() {
    if (this.isLoading || this.currentStatus !== "EN_CURSO") return

    this.setLoading(true)
    this.showToast("Marcando salida...", "info")

    try {
      const now = new Date()
      const timeString = now.toLocaleTimeString("es-ES", {
        hour: "2-digit",
        minute: "2-digit",
      })

      // Simular llamada a API
      const response = await this.makeApiCall("/empleados/asistencia/checkout/", {
        fecha: now.toISOString().split("T")[0],
        check_out: timeString,
        estado: "PRESENTE",
      })

      if (response.success) {
        this.checkOutTime = timeString
        this.updateStatus("PRESENTE")
        this.updateUI()
        this.calculateWorkedHours()
        this.showToast("¡Salida marcada correctamente!", "success")
      } else {
        throw new Error(response.error || "Error al marcar salida")
      }
    } catch (error) {
      this.showToast("Error al marcar salida: " + error.message, "error")
    } finally {
      this.setLoading(false)
    }
  }

  async makeApiCall(url, data) {
    // Llamada real a la API usando fetch
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').content
      },
      body: JSON.stringify(data)
    });
    return await response.json();
  }

  updateStatus(newStatus) {
    this.currentStatus = newStatus

    // Actualizar indicador de estado del empleado
    if (this.elements.employeeStatus) {
      this.elements.employeeStatus.className = "status-indicator " + newStatus.toLowerCase().replace("_", "-")
    }

    // Actualizar badge de estado
    if (this.elements.currentStatus) {
      const badge = this.elements.currentStatus.querySelector(".badge")
      if (badge) {
        badge.className = `badge badge-${newStatus.toLowerCase().replace("_", "-")}`
        badge.innerHTML = this.getStatusIcon(newStatus) + newStatus.replace("_", " ")
      }
    }

    // Actualizar estado en la tabla
    if (this.elements.todayStatus) {
      this.elements.todayStatus.className = `badge badge-${newStatus.toLowerCase().replace("_", "-")}`
      this.elements.todayStatus.innerHTML = this.getStatusIcon(newStatus) + newStatus.replace("_", " ")
    }
  }

  getStatusIcon(status) {
    switch (status) {
      case "PRESENTE":
        return '<i class="fas fa-check-circle"></i> '
      case "EN_CURSO":
        return '<i class="fas fa-clock"></i> '
      case "AUSENTE":
        return '<i class="fas fa-times-circle"></i> '
      default:
        return '<i class="fas fa-question-circle"></i> '
    }
  }

  updateUI() {
    // Mostrar/ocultar botones según el estado
    if (this.elements.quickCheckInBtn) {
      this.elements.quickCheckInBtn.style.display = this.currentStatus === "AUSENTE" ? "flex" : "none"
    }

    if (this.elements.quickCheckOutBtn) {
      this.elements.quickCheckOutBtn.style.display = this.currentStatus === "EN_CURSO" ? "flex" : "none"
    }

    if (this.elements.completedStatus) {
      this.elements.completedStatus.style.display = this.currentStatus === "PRESENTE" ? "flex" : "none"
    }

    // Actualizar información de tiempo
    if (this.elements.timeInfo) {
      this.elements.timeInfo.style.display = this.checkInTime || this.checkOutTime ? "block" : "none"
    }

    if (this.elements.entryTime && this.checkInTime) {
      this.elements.entryTime.style.display = "flex"
      if (this.elements.checkInTime) {
        this.elements.checkInTime.textContent = this.checkInTime
      }
    }

    if (this.elements.exitTime && this.checkOutTime) {
      this.elements.exitTime.style.display = "flex"
      if (this.elements.checkOutTime) {
        this.elements.checkOutTime.textContent = this.checkOutTime
      }
    }

    // Actualizar tabla de hoy
    if (this.elements.todayCheckIn) {
      this.elements.todayCheckIn.textContent = this.checkInTime || "--:--"
    }

    if (this.elements.todayCheckOut) {
      this.elements.todayCheckOut.textContent = this.checkOutTime || "--:--"
    }
  }

  calculateWorkedHours() {
    if (!this.checkInTime || !this.checkOutTime) return

    const [inHours, inMinutes] = this.checkInTime.split(":").map(Number)
    const [outHours, outMinutes] = this.checkOutTime.split(":").map(Number)

    const inTotalMinutes = inHours * 60 + inMinutes
    const outTotalMinutes = outHours * 60 + outMinutes
    const workedMinutes = outTotalMinutes - inTotalMinutes

    const hours = Math.floor(workedMinutes / 60)
    const minutes = workedMinutes % 60

    const workedHoursString = `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}`

    if (this.elements.workedHours) {
      this.elements.workedHours.textContent = `Horas trabajadas: ${workedHoursString}`
    }

    if (this.elements.todayHours) {
      this.elements.todayHours.textContent = workedHoursString
    }
  }

  setLoading(loading) {
    this.isLoading = loading

    if (this.elements.quickCheckInBtn) {
      this.elements.quickCheckInBtn.disabled = loading
      this.elements.quickCheckInBtn.classList.toggle("loading", loading)
    }

    if (this.elements.quickCheckOutBtn) {
      this.elements.quickCheckOutBtn.disabled = loading
      this.elements.quickCheckOutBtn.classList.toggle("loading", loading)
    }
  }

  loadTodayAttendance() {
    // Simular carga de asistencia del día actual
    // En producción, hacer llamada a API para obtener datos reales
    const savedCheckIn = localStorage.getItem("today_checkin")
    const savedCheckOut = localStorage.getItem("today_checkout")
    const savedStatus = localStorage.getItem("today_status")

    if (savedCheckIn) {
      this.checkInTime = savedCheckIn
    }

    if (savedCheckOut) {
      this.checkOutTime = savedCheckOut
    }

    if (savedStatus) {
      this.currentStatus = savedStatus
    }

    this.updateStatus(this.currentStatus)
    this.updateUI()

    if (this.checkInTime && this.checkOutTime) {
      this.calculateWorkedHours()
    }
  }

  showToast(message, type = "info") {
    const toastContainer = document.getElementById("toastContainer")
    if (!toastContainer) return

    const toast = document.createElement("div")
    toast.className = `toast ${type}`

    const icon = this.getToastIcon(type)
    toast.innerHTML = `${icon} ${message}`

    toastContainer.appendChild(toast)

    // Mostrar toast
    setTimeout(() => toast.classList.add("show"), 100)

    // Remover toast después de 4 segundos
    setTimeout(() => {
      toast.classList.remove("show")
      setTimeout(() => toast.remove(), 300)
    }, 4000)
  }

  getToastIcon(type) {
    switch (type) {
      case "success":
        return '<i class="fas fa-check-circle"></i>'
      case "error":
        return '<i class="fas fa-exclamation-circle"></i>'
      case "info":
        return '<i class="fas fa-info-circle"></i>'
      default:
        return '<i class="fas fa-bell"></i>'
    }
  }
}

// Clase para manejar filtros
class FiltrosAsistencia {
  constructor() {
    this.activeFilters = new Set()
    this.init()
  }

  init() {
    this.bindEvents()
  }

  bindEvents() {
    // Filtros pill
    const filterPills = document.querySelectorAll(".filter-pill")
    filterPills.forEach((pill) => {
      pill.addEventListener("click", (e) => this.handleFilterClick(e))
    })

    // Limpiar filtros
    const clearBtn = document.getElementById("clearFilters")
    if (clearBtn) {
      clearBtn.addEventListener("click", () => this.clearAllFilters())
    }

    // Búsqueda
    const searchInput = document.getElementById("busqueda")
    if (searchInput) {
      searchInput.addEventListener("input", (e) => this.handleSearch(e.target.value))
    }
  }

  handleFilterClick(e) {
    const pill = e.currentTarget
    const checkbox = pill.querySelector('input[type="checkbox"]')
    const filterType = pill.dataset.filter
    const filterValue = pill.dataset.value

    checkbox.checked = !checkbox.checked
    pill.classList.toggle("active", checkbox.checked)

    const filterKey = `${filterType}:${filterValue}`

    if (checkbox.checked) {
      this.activeFilters.add(filterKey)
    } else {
      this.activeFilters.delete(filterKey)
    }

    this.updateAppliedFilters()
    this.applyFilters()
  }

  updateAppliedFilters() {
    const appliedContainer = document.getElementById("appliedFilters")
    const appliedList = document.getElementById("appliedList")

    if (!appliedContainer || !appliedList) return

    if (this.activeFilters.size === 0) {
      appliedContainer.style.display = "none"
      return
    }

    appliedContainer.style.display = "flex"
    appliedList.innerHTML = ""

    this.activeFilters.forEach((filter) => {
      const [type, value] = filter.split(":")
      const item = document.createElement("div")
      item.className = "applied-item"
      item.innerHTML = `
        ${this.getFilterLabel(type, value)}
        <i class="fas fa-times" data-filter="${filter}"></i>
      `

      item.querySelector("i").addEventListener("click", () => this.removeFilter(filter))
      appliedList.appendChild(item)
    })
  }

  getFilterLabel(type, value) {
    const labels = {
      "estado:PRESENTE": "Presente",
      "estado:AUSENTE": "Ausente",
      "periodo:hoy": "Hoy",
      "periodo:semana": "Esta Semana",
      "periodo:mes": "Este Mes",
    }

    return labels[`${type}:${value}`] || value
  }

  removeFilter(filterKey) {
    this.activeFilters.delete(filterKey)

    // Desmarcar el checkbox correspondiente
    const [type, value] = filterKey.split(":")
    const pill = document.querySelector(`[data-filter="${type}"][data-value="${value}"]`)
    if (pill) {
      const checkbox = pill.querySelector('input[type="checkbox"]')
      checkbox.checked = false
      pill.classList.remove("active")
    }

    this.updateAppliedFilters()
    this.applyFilters()
  }

  clearAllFilters() {
    this.activeFilters.clear()

    // Desmarcar todos los checkboxes
    const checkboxes = document.querySelectorAll('.filter-pill input[type="checkbox"]')
    checkboxes.forEach((checkbox) => {
      checkbox.checked = false
      checkbox.closest(".filter-pill").classList.remove("active")
    })

    // Limpiar búsqueda
    const searchInput = document.getElementById("busqueda")
    if (searchInput) {
      searchInput.value = ""
    }

    this.updateAppliedFilters()
    this.applyFilters()
  }

  handleSearch(query) {
    // Implementar lógica de búsqueda
    console.log("Buscando:", query)
  }

  applyFilters() {
    // Implementar lógica de filtrado de tabla
    console.log("Aplicando filtros:", Array.from(this.activeFilters))
  }
}

// Inicializar cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", () => {
  new AsistenciaRapida()
  new FiltrosAsistencia()
})
