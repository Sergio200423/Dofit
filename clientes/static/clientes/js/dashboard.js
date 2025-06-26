document.addEventListener("DOMContentLoaded", () => {
  // Inicializar gráfico de distribución
  initDistributionChart()

  // Configurar modal de renovación
  setupRenewalModal()

  // Configurar filtro de período
  setupPeriodFilter()

  // Configurar botones de actualización
  setupRefreshButtons()
})

function initDistributionChart() {
  const ctx = document.getElementById("distribution-chart")
  if (!ctx) return

  // Obtener datos de los elementos HTML
  const diariaCount = Number.parseInt(document.getElementById("diaria-count").dataset.count) || 0
  const semanalCount = Number.parseInt(document.getElementById("semanal-count").dataset.count) || 0
  const quincenalCount = Number.parseInt(document.getElementById("quincenal-count").dataset.count) || 0
  const mensualCount = Number.parseInt(document.getElementById("mensual-count").dataset.count) || 0

  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Diaria", "Semanal", "Quincenal", "Mensual"],
      datasets: [
        {
          data: [diariaCount, semanalCount, quincenalCount, mensualCount],
          backgroundColor: ["#0066FF", "#4D94FF", "#80B5FF", "#B3D1FF"],
          borderWidth: 0,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
      },
      cutout: "70%",
    },
  })
}

function setupRenewalModal() {
  const modal = document.getElementById("renewModal")
  const renewButtons = document.querySelectorAll(".btn-renew")
  const closeBtn = document.querySelector(".close")
  const cancelBtn = document.querySelector(".btn-cancel")
  const form = document.getElementById("renewForm")

  if (!modal || !renewButtons.length) return

  // Abrir modal al hacer clic en botón de renovar
  renewButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const membershipId = this.dataset.id
      document.getElementById("membership-id").value = membershipId

      // Establecer fecha de inicio por defecto (hoy)
      const today = new Date()
      const formattedDate = today.toISOString().split("T")[0]
      document.getElementById("start-date").value = formattedDate

      modal.style.display = "block"
    })
  })

  // Cerrar modal
  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      modal.style.display = "none"
    })
  }

  if (cancelBtn) {
    cancelBtn.addEventListener("click", () => {
      modal.style.display = "none"
    })
  }

  // Cerrar modal al hacer clic fuera del contenido
  window.addEventListener("click", (event) => {
    if (event.target === modal) {
      modal.style.display = "none"
    }
  })

  // Manejar envío del formulario
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault()

      const membershipId = document.getElementById("membership-id").value
      const membershipType = document.getElementById("membership-type").value
      const startDate = document.getElementById("start-date").value

      // Aquí se enviaría la solicitud AJAX para renovar la membresía
      console.log("Renovando membresía:", {
        membershipId,
        membershipType,
        startDate,
      })

      // Simular éxito y cerrar modal
      setTimeout(() => {
        alert("Membresía renovada con éxito")
        modal.style.display = "none"

        // Recargar la página para ver los cambios
        window.location.reload()
      }, 1000)
    })
  }
}

function setupPeriodFilter() {
  const periodSelector = document.getElementById("period-selector")
  if (!periodSelector) return

  periodSelector.addEventListener("change", function () {
    const days = this.value

    // Aquí se enviaría una solicitud AJAX para filtrar las membresías
    // según el período seleccionado
    console.log("Filtrando por período:", days)

    // Recargar la página con el nuevo filtro
    // En producción, sería mejor actualizar solo las tablas necesarias
    if (days !== "all") {
      window.location.href = `?days=${days}`
    } else {
      window.location.href = "?"
    }
  })

  // Establecer el valor seleccionado según el parámetro de URL
  const urlParams = new URLSearchParams(window.location.search)
  const daysParam = urlParams.get("days")
  if (daysParam) {
    periodSelector.value = daysParam
  }
}

function setupRefreshButtons() {
  const refreshExpiringBtn = document.getElementById("refresh-expiring")
  const refreshExpiredBtn = document.getElementById("refresh-expired")

  if (refreshExpiringBtn) {
    refreshExpiringBtn.addEventListener("click", () => {
      // Aquí se enviaría una solicitud AJAX para actualizar la tabla
      // Por ahora, simplemente recargamos la página
      window.location.reload()
    })
  }

  if (refreshExpiredBtn) {
    refreshExpiredBtn.addEventListener("click", () => {
      window.location.reload()
    })
  }
}

// Función para contactar a un cliente
document.querySelectorAll(".btn-contact").forEach((button) => {
  button.addEventListener("click", function () {
    const clientId = this.dataset.id
    // Esta función podría abrir un modal de contacto o redirigir a una página de contacto
    console.log("Contactando al cliente:", clientId)
    alert("Función de contacto no implementada")
  })
})