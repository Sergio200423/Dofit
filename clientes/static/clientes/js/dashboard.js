document.addEventListener("DOMContentLoaded", () => {
  // Inicializar gráfico de distribución
  initDistributionChart()
  // Configurar modal de renovación
  setupRenewalModal()
  // Configurar filtro de período
  setupPeriodFilter()
  // Configurar botones de actualización
  setupRefreshButtons()
  // Configurar botón de impresión
  setupPrintButton()
})

let chartInstance = null

function initDistributionChart() {
  const ctx = document.getElementById("distribution-chart")
  if (!ctx) return

  // Obtener datos de los elementos HTML
  const diariaCount = Number.parseInt(document.getElementById("diaria-count").dataset.count) || 0
  const semanalCount = Number.parseInt(document.getElementById("semanal-count").dataset.count) || 0
  const quincenalCount = Number.parseInt(document.getElementById("quincenal-count").dataset.count) || 0
  const mensualCount = Number.parseInt(document.getElementById("mensual-count").dataset.count) || 0

  chartInstance = new Chart(ctx, {
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
        title: {
          display: true,
          text: "Distribución de Membresías",
          font: {
            size: 16,
            weight: "bold",
          },
          padding: {
            top: 10,
            bottom: 20,
          },
        },
      },
      cutout: "70%",
    },
  })
}

function setupPrintButton() {
  const printBtn = document.getElementById("print-chart")
  if (!printBtn) return

  printBtn.addEventListener("click", async () => {
    await generateChartPDF()
  })
}

async function generateChartPDF() {
  const loadingOverlay = document.getElementById("loading-overlay")
  const html2canvas = window.html2canvas

  try {
    // Mostrar loading
    loadingOverlay.style.display = "flex"

    // Crear un contenedor temporal para el PDF con mejor dimensionamiento
    const printContainer = document.createElement("div")
    printContainer.style.cssText = `
      position: absolute;
      top: -9999px;
      left: -9999px;
      width: 900px;
      height: 800px;
      background: white;
      padding: 50px;
      font-family: Arial, sans-serif;
      box-sizing: border-box;
    `
    document.body.appendChild(printContainer)

    // Crear el título
    const title = document.createElement("h1")
    title.textContent = "Distribución de Membresías - Gimnasio Dofit"
    title.style.cssText = `
      text-align: center;
      color: #333;
      margin-bottom: 40px;
      font-size: 28px;
      font-weight: bold;
    `
    printContainer.appendChild(title)

    // Crear contenedor para el gráfico con mejor dimensionamiento
    const chartContainer = document.createElement("div")
    chartContainer.style.cssText = `
      width: 500px;
      height: 400px;
      margin: 0 auto 40px;
      position: relative;
      display: flex;
      justify-content: center;
      align-items: center;
    `
    printContainer.appendChild(chartContainer)

    // Crear canvas temporal para el gráfico
    const tempCanvas = document.createElement("canvas")
    tempCanvas.width = 500
    tempCanvas.height = 400
    tempCanvas.style.cssText = `
      width: 500px;
      height: 400px;
    `
    chartContainer.appendChild(tempCanvas)

    // Obtener datos del gráfico original
    const diariaCount = Number.parseInt(document.getElementById("diaria-count").dataset.count) || 0
    const semanalCount = Number.parseInt(document.getElementById("semanal-count").dataset.count) || 0
    const quincenalCount = Number.parseInt(document.getElementById("quincenal-count").dataset.count) || 0
    const mensualCount = Number.parseInt(document.getElementById("mensual-count").dataset.count) || 0

    // Crear gráfico temporal con configuración mejorada
    const tempChart = new Chart(tempCanvas, {
      type: "doughnut",
      data: {
        labels: ["Diaria", "Semanal", "Quincenal", "Mensual"],
        datasets: [
          {
            data: [diariaCount, semanalCount, quincenalCount, mensualCount],
            backgroundColor: ["#0066FF", "#4D94FF", "#80B5FF", "#B3D1FF"],
            borderWidth: 3,
            borderColor: "#ffffff",
          },
        ],
      },
      options: {
        responsive: false,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: "bottom",
            labels: {
              padding: 25,
              font: {
                size: 16,
              },
              usePointStyle: true,
              pointStyle: "rect",
            },
          },
        },
        cutout: "65%",
        elements: {
          arc: {
            borderWidth: 3,
          },
        },
      },
    })

    // Esperar más tiempo para que el gráfico se renderice completamente
    await new Promise((resolve) => setTimeout(resolve, 2000))

    // Crear tabla de estadísticas con mejor layout
    const statsTable = document.createElement("div")
    statsTable.style.cssText = `
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 25px;
      margin-top: 40px;
      width: 100%;
      max-width: 600px;
      margin-left: auto;
      margin-right: auto;
    `

    const stats = [
      { label: "Diaria", value: diariaCount, color: "#0066FF" },
      { label: "Semanal", value: semanalCount, color: "#4D94FF" },
      { label: "Quincenal", value: quincenalCount, color: "#80B5FF" },
      { label: "Mensual", value: mensualCount, color: "#B3D1FF" },
    ]

    stats.forEach((stat) => {
      const statItem = document.createElement("div")
      statItem.style.cssText = `
        display: flex;
        align-items: center;
        padding: 20px;
        border: 2px solid #eee;
        border-radius: 12px;
        background-color: #fafafa;
        min-height: 60px;
        box-sizing: border-box;
      `

      statItem.innerHTML = `
        <div style="width: 25px; height: 25px; background-color: ${stat.color}; border-radius: 6px; margin-right: 20px; flex-shrink: 0;"></div>
        <div style="flex: 1;">
          <div style="font-weight: bold; font-size: 22px; color: #333; margin-bottom: 5px;">${stat.value}</div>
          <div style="color: #666; font-size: 16px;">${stat.label}</div>
        </div>
      `
      statsTable.appendChild(statItem)
    })

    printContainer.appendChild(statsTable)

    // Agregar fecha de generación
    const dateInfo = document.createElement("div")
    dateInfo.style.cssText = `
      text-align: center;
      margin-top: 50px;
      color: #666;
      font-size: 14px;
      padding-top: 20px;
      border-top: 1px solid #eee;
    `
    dateInfo.textContent = `Generado el: ${new Date().toLocaleDateString("es-ES", {
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })}`
    printContainer.appendChild(dateInfo)

    // Capturar el contenedor como imagen con mejor calidad
    const canvas = await html2canvas(printContainer, {
      scale: 3,
      useCORS: true,
      allowTaint: true,
      backgroundColor: "#ffffff",
      width: 900,
      height: 800,
      logging: false,
    })

    // Crear PDF con mejor configuración
    const { jsPDF } = window.jspdf
    const pdf = new jsPDF({
      orientation: "portrait",
      unit: "mm",
      format: "a4",
    })

    const imgData = canvas.toDataURL("image/png", 1.0)
    const pdfWidth = pdf.internal.pageSize.getWidth()
    const pdfHeight = pdf.internal.pageSize.getHeight()

    // Calcular dimensiones manteniendo proporción
    const imgWidth = pdfWidth - 20 // 10mm margen cada lado
    const imgHeight = (canvas.height * imgWidth) / canvas.width

    // Centrar verticalmente
    const x = 10
    const y = Math.max(10, (pdfHeight - imgHeight) / 2)

    // Agregar imagen al PDF
    pdf.addImage(imgData, "PNG", x, y, imgWidth, imgHeight, undefined, "FAST")

    // Descargar PDF
    const fileName = `distribucion-membresias-${new Date().toISOString().split("T")[0]}.pdf`
    pdf.save(fileName)

    // Limpiar recursos
    tempChart.destroy()
    document.body.removeChild(printContainer)

    // Mostrar mensaje de éxito
    setTimeout(() => {
      alert("PDF generado exitosamente")
    }, 500)
  } catch (error) {
    console.error("Error al generar PDF:", error)
    alert("Error al generar el PDF. Por favor, inténtelo de nuevo.")
  } finally {
    // Ocultar loading
    loadingOverlay.style.display = "none"
  }
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
