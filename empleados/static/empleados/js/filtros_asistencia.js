// Clase mejorada para manejar filtros, paginación y exportación
class FiltrosAsistenciaAvanzados {
  constructor() {
    this.activeFilters = new Map()
    this.currentPage = 1
    this.itemsPerPage = 10
    this.allRows = []
    this.filteredRows = []
    this.sortColumn = null
    this.sortDirection = "asc"
    this.searchQuery = ""

    this.init()
  }

  init() {
    // Esperar a que la tabla esté cargada
    setTimeout(() => {
      this.cacheTableRows()
      this.bindEvents()
      this.setupPagination()
    }, 100)
  }

  cacheTableRows() {
    const tbody = document.querySelector("#tablaAsistencias tbody")
    if (tbody) {
      // Excluir la fila de "hoy" del filtrado
      this.allRows = Array.from(tbody.querySelectorAll("tr:not(.today-row):not(.empty-row)"))
      this.filteredRows = [...this.allRows]
      console.log("Filas cacheadas:", this.allRows.length)
    }
  }

  bindEvents() {
    // Filtros pill - Corregir el event binding
    const filterPills = document.querySelectorAll(".filter-pill")
    console.log("Filter pills encontrados:", filterPills.length)

    filterPills.forEach((pill) => {
      pill.addEventListener("click", (e) => {
        e.preventDefault()
        e.stopPropagation()
        console.log("Clic en filtro:", pill.dataset.filter, pill.dataset.value)
        this.handleFilterClick(pill)
      })
    })

    // Limpiar filtros
    const clearBtn = document.getElementById("clearFilters")
    if (clearBtn) {
      clearBtn.addEventListener("click", (e) => {
        e.preventDefault()
        console.log("Limpiando filtros")
        this.clearAllFilters()
      })
    }

    // Búsqueda
    const searchInput = document.getElementById("busqueda")
    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        console.log("Búsqueda:", e.target.value)
        this.handleSearch(e.target.value)
      })
    }

    // Exportar
    const exportBtn = document.querySelector(".btn-export")
    if (exportBtn) {
      exportBtn.addEventListener("click", (e) => {
        e.preventDefault()
        console.log("Exportando datos")
        this.exportData()
      })
    }

    // Ordenamiento de tabla
    const sortableHeaders = document.querySelectorAll(".sortable")
    sortableHeaders.forEach((header) => {
      header.addEventListener("click", () => {
        const sortKey = header.dataset.sort
        console.log("Ordenando por:", sortKey)
        this.handleSort(sortKey, header)
      })
    })

    // Paginación
    this.bindPaginationEvents()
  }

  handleFilterClick(pill) {
    const checkbox = pill.querySelector('input[type="checkbox"]')
    const filterType = pill.dataset.filter
    const filterValue = pill.dataset.value

    if (!checkbox || !filterType || !filterValue) {
      console.log("Datos de filtro incompletos")
      return
    }

    // Toggle del checkbox
    checkbox.checked = !checkbox.checked
    console.log("Checkbox estado:", checkbox.checked)

    const filterKey = `${filterType}:${filterValue}`

    if (checkbox.checked) {
      this.activeFilters.set(filterKey, { type: filterType, value: filterValue })
      console.log("Filtro agregado:", filterKey)
    } else {
      this.activeFilters.delete(filterKey)
      console.log("Filtro removido:", filterKey)
    }

    this.updateAppliedFilters()
    this.applyFilters()
  }

  handleSearch(query) {
    this.searchQuery = query.toLowerCase().trim()
    console.log("Búsqueda aplicada:", this.searchQuery)
    this.applyFilters()
  }

  handleSort(column, headerElement) {
    // Actualizar dirección de ordenamiento
    if (this.sortColumn === column) {
      this.sortDirection = this.sortDirection === "asc" ? "desc" : "asc"
    } else {
      this.sortColumn = column
      this.sortDirection = "asc"
    }

    // Actualizar iconos de ordenamiento
    document.querySelectorAll(".sortable i").forEach((icon) => {
      icon.className = "fas fa-sort"
    })

    const icon = headerElement.querySelector("i")
    if (icon) {
      icon.className = `fas fa-sort-${this.sortDirection === "asc" ? "up" : "down"}`
    }

    this.sortRows()
    this.applyFilters()
  }

  sortRows() {
    // Implementar ordenamiento básico
    this.filteredRows.sort((a, b) => {
      let aValue, bValue

      switch (this.sortColumn) {
        case "fecha":
          aValue = a.querySelector(".date-main")?.textContent || ""
          bValue = b.querySelector(".date-main")?.textContent || ""
          break
        case "checkin":
          aValue = a.querySelector(".col-checkin")?.textContent.trim() || ""
          bValue = b.querySelector(".col-checkin")?.textContent.trim() || ""
          break
        case "checkout":
          aValue = a.querySelector(".col-checkout")?.textContent.trim() || ""
          bValue = b.querySelector(".col-checkout")?.textContent.trim() || ""
          break
        case "estado":
          aValue = a.querySelector(".badge")?.textContent.trim() || ""
          bValue = b.querySelector(".badge")?.textContent.trim() || ""
          break
        default:
          return 0
      }

      if (aValue < bValue) return this.sortDirection === "asc" ? -1 : 1
      if (aValue > bValue) return this.sortDirection === "asc" ? 1 : -1
      return 0
    })
  }

  applyFilters() {
    console.log("Aplicando filtros. Total filas:", this.allRows.length)
    console.log("Filtros activos:", Array.from(this.activeFilters.keys()))
    console.log("Búsqueda:", this.searchQuery)

    this.filteredRows = this.allRows.filter((row) => {
      // Filtro de búsqueda
      if (this.searchQuery) {
        const rowText = row.textContent.toLowerCase()
        if (!rowText.includes(this.searchQuery)) {
          return false
        }
      }

      // Filtros de estado y período
      for (const [key, filter] of this.activeFilters) {
        if (filter.type === "estado") {
          const badge = row.querySelector(".badge")
          const estado = badge?.textContent.trim().toUpperCase()
          if (!estado || !estado.includes(filter.value)) {
            return false
          }
        }

        if (filter.type === "periodo") {
          if (!this.matchesPeriodFilter(row, filter.value)) {
            return false
          }
        }
      }

      return true
    })

    console.log("Filas filtradas:", this.filteredRows.length)

    this.currentPage = 1
    this.updatePagination()
    this.displayCurrentPage()
  }

  matchesPeriodFilter(row, periodo) {
    const dateCell = row.querySelector(".date-main")
    if (!dateCell) return false

    const today = new Date()
    const dateText = dateCell.textContent.trim()

    // Si es "Hoy", siempre coincide con el filtro "hoy"
    if (dateText === "Hoy" && periodo === "hoy") {
      return true
    }

    // Para otras fechas, intentar parsear
    try {
      const rowDate = this.parseDate(dateText)

      switch (periodo) {
        case "hoy":
          return this.isSameDay(rowDate, today)
        case "semana":
          return this.isThisWeek(rowDate, today)
        case "mes":
          return this.isThisMonth(rowDate, today)
        default:
          return true
      }
    } catch (e) {
      console.log("Error parseando fecha:", dateText)
      return false
    }
  }

  parseDate(dateText) {
    // Intentar parsear diferentes formatos de fecha
    if (dateText === "Hoy") {
      return new Date()
    }

    // Formato "28 Jun" o similar
    const months = {
      Ene: 0,
      Feb: 1,
      Mar: 2,
      Abr: 3,
      May: 4,
      Jun: 5,
      Jul: 6,
      Ago: 7,
      Sep: 8,
      Oct: 9,
      Nov: 10,
      Dic: 11,
    }

    const parts = dateText.split(" ")
    if (parts.length >= 2) {
      const day = Number.parseInt(parts[0])
      const month = months[parts[1]]
      if (!isNaN(day) && month !== undefined) {
        return new Date(2025, month, day)
      }
    }

    return new Date(dateText)
  }

  isSameDay(date1, date2) {
    return date1.toDateString() === date2.toDateString()
  }

  isThisWeek(date, today) {
    const startOfWeek = new Date(today)
    startOfWeek.setDate(today.getDate() - today.getDay())
    const endOfWeek = new Date(startOfWeek)
    endOfWeek.setDate(startOfWeek.getDate() + 6)
    return date >= startOfWeek && date <= endOfWeek
  }

  isThisMonth(date, today) {
    return date.getMonth() === today.getMonth() && date.getFullYear() === today.getFullYear()
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

    this.activeFilters.forEach((filter, key) => {
      const item = document.createElement("div")
      item.className = "applied-item"
      item.innerHTML = `
        ${this.getFilterLabel(filter.type, filter.value)}
        <i class="fas fa-times" data-filter="${key}"></i>
      `

      item.querySelector("i").addEventListener("click", (e) => {
        e.stopPropagation()
        this.removeFilter(key)
      })
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
      if (checkbox) {
        checkbox.checked = false
      }
    }

    this.updateAppliedFilters()
    this.applyFilters()
  }

  clearAllFilters() {
    this.activeFilters.clear()
    this.searchQuery = ""

    // Desmarcar todos los checkboxes
    const checkboxes = document.querySelectorAll('.filter-pill input[type="checkbox"]')
    checkboxes.forEach((checkbox) => {
      checkbox.checked = false
    })

    // Limpiar búsqueda
    const searchInput = document.getElementById("busqueda")
    if (searchInput) {
      searchInput.value = ""
    }

    this.updateAppliedFilters()
    this.applyFilters()
  }

  setupPagination() {
    this.updatePagination()
  }

  bindPaginationEvents() {
    const paginationContainer = document.querySelector(".pagination-controls")
    if (paginationContainer) {
      paginationContainer.addEventListener("click", (e) => {
        if (e.target.classList.contains("page-btn")) {
          e.preventDefault()
          this.handlePageClick(e.target)
        }
      })
    }
  }

  handlePageClick(button) {
    if (button.disabled) return

    if (button.classList.contains("prev-btn")) {
      if (this.currentPage > 1) {
        this.currentPage--
      }
    } else if (button.classList.contains("next-btn")) {
      const totalPages = Math.ceil(this.filteredRows.length / this.itemsPerPage)
      if (this.currentPage < totalPages) {
        this.currentPage++
      }
    } else if (!isNaN(button.textContent)) {
      this.currentPage = Number.parseInt(button.textContent)
    }

    this.updatePagination()
    this.displayCurrentPage()
  }

  updatePagination() {
    const totalItems = this.filteredRows.length
    const totalPages = Math.ceil(totalItems / this.itemsPerPage)

    // Actualizar información de paginación
    const paginationInfo = document.querySelector(".pagination-info")
    if (paginationInfo) {
      const startItem = totalItems > 0 ? (this.currentPage - 1) * this.itemsPerPage + 1 : 0
      const endItem = Math.min(this.currentPage * this.itemsPerPage, totalItems)
      paginationInfo.innerHTML = `
        Mostrando <strong>${startItem}</strong> a <strong>${endItem}</strong> de <strong>${totalItems}</strong> registros
      `
    }

    // Actualizar controles de paginación
    const paginationControls = document.querySelector(".pagination-controls")
    if (paginationControls) {
      paginationControls.innerHTML = this.generatePaginationHTML(totalPages)
    }
  }

  generatePaginationHTML(totalPages) {
    let html = `
      <button class="page-btn prev-btn" ${this.currentPage <= 1 ? "disabled" : ""}>
        <i class="fas fa-chevron-left"></i>
      </button>
    `

    // Generar botones de página
    const startPage = Math.max(1, this.currentPage - 2)
    const endPage = Math.min(totalPages, this.currentPage + 2)

    for (let i = startPage; i <= endPage; i++) {
      html += `
        <button class="page-btn ${i === this.currentPage ? "active" : ""}">${i}</button>
      `
    }

    html += `
      <button class="page-btn next-btn" ${this.currentPage >= totalPages ? "disabled" : ""}>
        <i class="fas fa-chevron-right"></i>
      </button>
    `

    return html
  }

  displayCurrentPage() {
    console.log("Mostrando página:", this.currentPage)

    // Ocultar todas las filas (excepto la de hoy)
    this.allRows.forEach((row) => {
      row.style.display = "none"
    })

    // Mostrar filas de la página actual
    const startIndex = (this.currentPage - 1) * this.itemsPerPage
    const endIndex = startIndex + this.itemsPerPage
    const pageRows = this.filteredRows.slice(startIndex, endIndex)

    console.log("Mostrando filas:", pageRows.length, "de", this.filteredRows.length)

    pageRows.forEach((row) => {
      row.style.display = ""
    })

    // Mostrar mensaje si no hay resultados
    this.toggleEmptyState(this.filteredRows.length === 0)
  }

  toggleEmptyState(show) {
    let emptyRow = document.querySelector(".empty-row")

    if (show && !emptyRow) {
      const tbody = document.querySelector("#tablaAsistencias tbody")
      emptyRow = document.createElement("tr")
      emptyRow.className = "empty-row"
      emptyRow.innerHTML = `
        <td colspan="6">
          <div class="empty-state">
            <i class="fas fa-search"></i>
            <p>No se encontraron registros con los filtros aplicados</p>
          </div>
        </td>
      `
      tbody.appendChild(emptyRow)
    } else if (!show && emptyRow) {
      emptyRow.remove()
    }
  }

  exportData() {
    const data = this.prepareExportData()
    this.downloadCSV(data, "asistencia_export.csv")
    this.showToast("Datos exportados correctamente", "success")
  }

  prepareExportData() {
    const headers = ["Fecha", "Check-in", "Check-out", "Horas", "Estado"]
    const rows = [headers]

    this.filteredRows.forEach((row) => {
      const fecha = row.querySelector(".date-main")?.textContent || ""
      const checkin = row.querySelector(".col-checkin")?.textContent.trim() || "--:--"
      const checkout = row.querySelector(".col-checkout")?.textContent.trim() || "--:--"
      const horas = row.querySelector(".col-horas")?.textContent.trim() || "00:00"
      const estado = row.querySelector(".badge")?.textContent.trim() || ""

      rows.push([fecha, checkin, checkout, horas, estado])
    })

    return rows
  }

  downloadCSV(data, filename) {
    const csvContent = data.map((row) => row.map((cell) => `"${cell}"`).join(",")).join("\n")
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" })
    const link = document.createElement("a")

    if (link.download !== undefined) {
      const url = URL.createObjectURL(blob)
      link.setAttribute("href", url)
      link.setAttribute("download", filename)
      link.style.visibility = "hidden"
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  }

  showToast(message, type = "info") {
    const toastContainer = document.getElementById("toastContainer")
    if (!toastContainer) return

    const toast = document.createElement("div")
    toast.className = `toast ${type}`

    const icon = type === "success" ? '<i class="fas fa-check-circle"></i>' : '<i class="fas fa-info-circle"></i>'

    toast.innerHTML = `${icon} ${message}`

    toastContainer.appendChild(toast)

    setTimeout(() => toast.classList.add("show"), 100)
    setTimeout(() => {
      toast.classList.remove("show")
      setTimeout(() => toast.remove(), 300)
    }, 4000)
  }
}

// Inicializar cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", () => {
  console.log("Inicializando filtros de asistencia")
  window.filtrosAsistencia = new FiltrosAsistenciaAvanzados()
})
