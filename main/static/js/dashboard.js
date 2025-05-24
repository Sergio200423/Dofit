import { Chart } from "@/components/ui/chart"
document.addEventListener("DOMContentLoaded", () => {
  // Datos simulados para el dashboard
  const salesData = {
    labels: ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
    datasets: [
      {
        label: "Ventas diarias",
        data: [12500, 18200, 15800, 22400, 19800, 28500, 24200],
        borderColor: "#0066ff",
        backgroundColor: "rgba(0, 102, 255, 0.1)",
        tension: 0.4,
        fill: true,
      },
    ],
  }

  const distributionData = {
    labels: ["Proteínas", "Pre-entrenos", "Accesorios", "Membresías", "Otros"],
    datasets: [
      {
        data: [35, 20, 15, 25, 5],
        backgroundColor: ["#0066ff", "#28a745", "#ffc107", "#dc3545", "#6c757d"],
        borderWidth: 0,
      },
    ],
  }

  // Productos más vendidos
  const topProducts = [
    { name: "Proteína Whey", category: "Suplementos", sales: 124, revenue: 3719.76 },
    { name: "Pre-entreno", category: "Suplementos", sales: 98, revenue: 1959.02 },
    { name: "Membresía Premium", category: "Membresías", sales: 87, revenue: 6089.13 },
    { name: "Shaker", category: "Accesorios", sales: 76, revenue: 607.24 },
    { name: "Guantes de Entrenamiento", category: "Accesorios", sales: 65, revenue: 974.35 },
  ]

  // Últimas ventas
  const recentSales = [
    { client: "Juan Pérez", date: "07/05/2025", items: 3, total: 89.97, status: "completed" },
    { client: "María García", date: "07/05/2025", items: 1, total: 69.99, status: "completed" },
    { client: "Carlos López", date: "06/05/2025", items: 2, total: 37.98, status: "pending" },
    { client: "Ana Martínez", date: "06/05/2025", items: 5, total: 127.45, status: "completed" },
    { client: "Roberto Sánchez", date: "05/05/2025", items: 1, total: 29.99, status: "cancelled" },
    { client: "Laura Rodríguez", date: "05/05/2025", items: 2, total: 49.98, status: "completed" },
    { client: "Pedro Gómez", date: "04/05/2025", items: 4, total: 112.96, status: "completed" },
  ]

  // Inicializar gráficos
  const salesChart = new Chart(document.getElementById("sales-chart"), {
    type: "line",
    data: salesData,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          callbacks: {
            label: (context) => `C$${context.raw.toLocaleString()}`,
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: (value) => {
              if (value >= 1000) {
                return "C$" + value / 1000 + "k"
              }
              return "C$" + value
            },
          },
        },
      },
    },
  })

  const distributionChart = new Chart(document.getElementById("distribution-chart"), {
    type: "doughnut",
    data: distributionData,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          callbacks: {
            label: (context) => `${context.label}: ${context.raw}%`,
          },
        },
      },
      cutout: "70%",
    },
  })

  // Crear leyenda personalizada para el gráfico de distribución
  const legendContainer = document.getElementById("distribution-legend")
  distributionData.labels.forEach((label, index) => {
    const color = distributionData.datasets[0].backgroundColor[index]
    const percentage = distributionData.datasets[0].data[index]

    const legendItem = document.createElement("div")
    legendItem.className = "legend-item"
    legendItem.innerHTML = `
            <span class="legend-color" style="background-color: ${color}"></span>
            <span>${label}: ${percentage}%</span>
        `

    legendContainer.appendChild(legendItem)
  })

  // Cargar productos más vendidos
  const topProductsBody = document.getElementById("top-products-body")
  topProducts.forEach((product) => {
    const row = document.createElement("tr")
    row.innerHTML = `
            <td>${product.name}</td>
            <td>${product.category}</td>
            <td>${product.sales}</td>
            <td>C$${product.revenue.toFixed(2)}</td>
        `
    topProductsBody.appendChild(row)
  })

  // Cargar últimas ventas
  const recentSalesBody = document.getElementById("recent-sales-body")
  recentSales.forEach((sale) => {
    const row = document.createElement("tr")
    row.innerHTML = `
            <td>${sale.client}</td>
            <td>${sale.date}</td>
            <td>${sale.items}</td>
            <td>C$${sale.total.toFixed(2)}</td>
            <td><span class="status ${sale.status}">${getStatusText(sale.status)}</span></td>
        `
    recentSalesBody.appendChild(row)
  })

  // Actualizar tarjetas de resumen
  document.getElementById("total-ventas").textContent = "C$141,000"
  document.getElementById("total-transacciones").textContent = "487"
  document.getElementById("nuevos-clientes").textContent = "64"
  document.getElementById("nuevas-membresias").textContent = "87"

  // Cambiar tipo de gráfico
  document.querySelectorAll(".btn-chart-type").forEach((button) => {
    button.addEventListener("click", function () {
      const chartType = this.getAttribute("data-type")

      // Actualizar botones activos
      document.querySelectorAll(".btn-chart-type").forEach((btn) => {
        btn.classList.remove("active")
      })
      this.classList.add("active")

      // Cambiar tipo de gráfico
      salesChart.config.type = chartType
      salesChart.update()
    })
  })

  // Función para obtener texto de estado
  function getStatusText(status) {
    switch (status) {
      case "completed":
        return "Completado"
      case "pending":
        return "Pendiente"
      case "cancelled":
        return "Cancelado"
      default:
        return status
    }
  }

  // Evento para selector de período
  document.getElementById("period-selector").addEventListener("change", function () {
    const days = Number.parseInt(this.value)
    updateChartData(days)
  })

  // Función para actualizar datos del gráfico según el período
  function updateChartData(days) {
    // Aquí normalmente harías una petición AJAX para obtener datos reales
    // Para este ejemplo, generamos datos aleatorios

    let labels = []
    const data = []

    if (days <= 7) {
      // Datos diarios para la última semana
      labels = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
      for (let i = 0; i < 7; i++) {
        data.push(Math.floor(Math.random() * 20000) + 10000)
      }
    } else if (days <= 30) {
      // Datos para el último mes (4 semanas)
      labels = ["Semana 1", "Semana 2", "Semana 3", "Semana 4"]
      for (let i = 0; i < 4; i++) {
        data.push(Math.floor(Math.random() * 80000) + 40000)
      }
    } else if (days <= 90) {
      // Datos para los últimos 3 meses
      labels = ["Marzo", "Abril", "Mayo"]
      for (let i = 0; i < 3; i++) {
        data.push(Math.floor(Math.random() * 250000) + 150000)
      }
    } else {
      // Datos para el último año
      labels = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
      for (let i = 0; i < 12; i++) {
        data.push(Math.floor(Math.random() * 300000) + 200000)
      }
    }

    salesChart.data.labels = labels
    salesChart.data.datasets[0].data = data
    salesChart.update()
  }

  // Botón de actualizar
  document.querySelector(".btn-refresh").addEventListener("click", function () {
    this.classList.add("fa-spin")
    setTimeout(() => {
      this.classList.remove("fa-spin")
      // Aquí normalmente harías una petición AJAX para obtener datos actualizados
    }, 1000)
  })
})
