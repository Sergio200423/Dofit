// Función para formatear moneda
function formatCurrency(amount) {
  return "C$ " + amount.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, "$&,")
}

// Función para formatear fecha
function formatDate(dateString) {
  const options = { year: "numeric", month: "long", day: "numeric" }
  return new Date(dateString).toLocaleDateString("es-ES", options)
}

// Función para cargar los datos del cliente
function loadClientData(client) {
  document.getElementById("client-name").textContent = client.nombre
  document.getElementById("client-email").textContent = client.email
}

// Función para cargar los datos del resumen de pago
function loadPaymentSummary(payment, discounts, products) {
  // Calcular totales
  const totalPayment = payment.total_original
  const totalDiscounts = discounts.reduce((sum, discount) => sum + discount.monto, 0)
  const totalProducts = products.length
  const finalTotal = payment.total_a_pagar

  // Actualizar elementos en el DOM
  document.getElementById("total-payments").textContent = formatCurrency(totalPayment)
  document.getElementById("total-discounts").textContent = formatCurrency(totalDiscounts)
  document.getElementById("total-products").textContent = totalProducts
  document.getElementById("final-total").textContent = formatCurrency(finalTotal)
}

// Función para cargar los detalles del pago
function loadPaymentDetails(payment) {
  document.getElementById("payment-id").textContent = payment.id_pago
  document.getElementById("payment-date").textContent = formatDate(payment.fecha)
  document.getElementById("payment-type").textContent = payment.tipo
  document.getElementById("payment-client").textContent = payment.cliente.nombre
  document.getElementById("payment-original").textContent = formatCurrency(payment.total_original)
  document.getElementById("payment-final").textContent = formatCurrency(payment.total_a_pagar)
}

// Función para cargar la tabla de descuentos
function loadDiscountsTable(discounts) {
  const tableBody = document.querySelector("#discounts-table tbody")
  tableBody.innerHTML = ""

  if (discounts.length === 0) {
    const row = document.createElement("tr")
    row.innerHTML = `<td colspan="3" class="text-center">No hay descuentos aplicados</td>`
    tableBody.appendChild(row)
    return
  }

  discounts.forEach((discount) => {
    const row = document.createElement("tr")
    row.innerHTML = `
            <td>${discount.nombre}</td>
            <td>${formatCurrency(discount.monto)}</td>
            <td>${discount.descripcion || "-"}</td>
        `
    tableBody.appendChild(row)
  })
}

// Función para cargar la tabla de productos
function loadProductsTable(products) {
  const tableBody = document.querySelector("#products-table tbody")
  tableBody.innerHTML = ""

  if (products.length === 0) {
    const row = document.createElement("tr")
    row.innerHTML = `<td colspan="4" class="text-center">No hay productos comprados</td>`
    tableBody.appendChild(row)
    return
  }

  products.forEach((product) => {
    const row = document.createElement("tr")
    row.innerHTML = `
            <td>${product.nombre_producto}</td>
            <td>${product.cantidad}</td>
            <td>${formatCurrency(product.precio)}</td>
            <td>${formatCurrency(product.total)}</td>
        `
    tableBody.appendChild(row)
  })
}

// Función para inicializar el gráfico
function initChart(data, label = 'Pagos Anuales') {
  const ctx = document.getElementById("payments-chart").getContext("2d")
  if (window.paymentsChart) {
    window.paymentsChart.destroy();
  }
  window.paymentsChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: data.map((item) => item.month),
      datasets: [
        {
          label: label,
          data: data.map((item) => item.amount),
          backgroundColor: "#4F46E5",
          borderColor: "#4F46E5",
          borderWidth: 1,
          borderRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: "#E5E7EB",
          },
          ticks: {
            callback: (value) => "C$ " + value,
          },
        },
        x: {
          grid: {
            display: false,
          },
        },
      },
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          callbacks: {
            label: (context) => "C$ " + context.raw,
          },
        },
      },
    },
  });

  // Manejar los botones de filtro
  document.querySelectorAll(".filter-btn").forEach((button) => {
    button.addEventListener("click", function () {
      document.querySelectorAll(".filter-btn").forEach((btn) => btn.classList.remove("active"))
      this.classList.add("active")
      const period = this.dataset.period
      let labels = [];
      let values = [];
      let chartLabel = '';
      if (period === "weekly") {
        labels = historialSemanalLabels;
        values = historialSemanalData;
        chartLabel = "Pagos Semanales";
      } else if (period === "monthly") {
        labels = historialMensualLabels;
        values = historialMensualData;
        chartLabel = "Pagos Mensuales";
      } else {
        labels = historialAnualLabels;
        values = historialAnualData;
        chartLabel = "Pagos Anuales";
      }
      window.paymentsChart.data.labels = labels;
      window.paymentsChart.data.datasets[0].data = values;
      window.paymentsChart.data.datasets[0].label = chartLabel;
      window.paymentsChart.update();
    })
  })
}

// Función para manejar la descarga del PDF
function setupPDFDownload() {
  document.getElementById("download-pdf").addEventListener("click", () => {
    alert("Descargando reporte en PDF...")
    // Aquí puedes implementar la lógica real de descarga si lo deseas
  })
}

// Función para manejar la impresión
function setupPrint() {
  document.getElementById("print-report").addEventListener("click", () => {
    window.print()
  })
}

// Inicializar la aplicación con datos reales del backend y los datos de los context variables de Django

document.addEventListener("DOMContentLoaded", () => {
  // Quitar displayCurrentDate(); porque no existe el elemento en el HTML
  // displayCurrentDate();
  setupPDFDownload();
  setupPrint();

  // Depuración: Verifica si el canvas existe y los datos están bien
  const canvas = document.getElementById("payments-chart");
  if (!canvas) {
    console.error("No se encontró el canvas con id 'payments-chart'");
  } else {
    console.log("Canvas encontrado correctamente");
  }
  console.log("historialAnualLabels:", historialAnualLabels);
  console.log("historialAnualData:", historialAnualData);

  // Inicializar el gráfico con datos anuales por defecto
  if (typeof historialAnualLabels !== 'undefined' && typeof historialAnualData !== 'undefined' && Array.isArray(historialAnualLabels) && Array.isArray(historialAnualData) && historialAnualLabels.length > 0) {
    const chartData = historialAnualLabels.map(function(label, idx) {
      return {
        month: label,
        amount: historialAnualData[idx]
      };
    });
    console.log("chartData para initChart:", chartData);
    initChart(chartData, 'Pagos Anuales');
  } else {
    console.warn("No hay datos anuales para el gráfico o los datos no son válidos");
  }
});

function generatePDF() {
  // Mostrar mensaje de carga
  const loadingMessage = document.createElement("div");
  loadingMessage.style.position = "fixed";
  loadingMessage.style.top = "0";
  loadingMessage.style.left = "0";
  loadingMessage.style.width = "100%";
  loadingMessage.style.height = "100%";
  loadingMessage.style.backgroundColor = "rgba(255, 255, 255, 0.8)";
  loadingMessage.style.display = "flex";
  loadingMessage.style.justifyContent = "center";
  loadingMessage.style.alignItems = "center";
  loadingMessage.style.zIndex = "9999";
  loadingMessage.innerHTML = '<div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);"><h3>Generando PDF...</h3><p>Por favor espere, esto puede tomar unos momentos.</p></div>';
  document.body.appendChild(loadingMessage);

  // Guardar el estado actual de la página
  const paginationControls = document.querySelectorAll('.pagination-controls');
  const paymentItems = document.querySelectorAll('.payment-item');
  const currentPageState = getCurrentPageState();
  
  // Ocultar controles de paginación para el PDF
  paginationControls.forEach(control => {
    control.style.display = 'none';
  });
  
  // Mostrar TODOS los elementos de pago para capturarlos
  paymentItems.forEach(item => {
    item.style.display = 'block';
  });
  
  // Dar tiempo al navegador para renderizar los cambios
  setTimeout(() => {
    // Importar jsPDF
    const { jsPDF } = window.jspdf;

    // Crear una nueva instancia de jsPDF
    const doc = new jsPDF('p', 'mm', 'a4');
    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();
    const margin = 10;

    // Capturar las secciones principales
    const summarySection = document.querySelector('.payment-summary');
    const chartSection = document.querySelector('.chart-section');
    const detailsSection = document.querySelector('.payment-details');

    // Primero capturamos el título y el resumen
    html2canvas(summarySection, {
      scale: 2,
      useCORS: true,
      logging: false,
      allowTaint: true
    }).then(canvas => {
      const imgData = canvas.toDataURL('image/png');
      const imgWidth = pageWidth - margin * 2;
      const imgHeight = (canvas.height * imgWidth) / canvas.width;

      // Añadir título
      doc.setFontSize(18);
      doc.text('Reporte de Pagos - Gimnasio Dofit', pageWidth / 2, margin, { align: 'center' });

      // Añadir fecha
      doc.setFontSize(12);
      doc.text(`Generado el: ${new Date().toLocaleDateString()}`, pageWidth / 2, margin + 8, { align: 'center' });

      // Añadir el resumen
      doc.addImage(imgData, 'PNG', margin, margin + 15, imgWidth, imgHeight);
      
      let currentY = margin + 15 + imgHeight + 10;

      // Luego capturamos el gráfico
      return html2canvas(chartSection, {
        scale: 2,
        useCORS: true,
        logging: false,
        allowTaint: true
      }).then(canvas => {
        const imgData = canvas.toDataURL('image/png');
        const imgWidth = pageWidth - margin * 2;
        const imgHeight = (canvas.height * imgWidth) / canvas.width;

        // Verificar si hay espacio suficiente en la página actual
        if (currentY + imgHeight > pageHeight - margin) {
          doc.addPage();
          currentY = margin;
        }

        // Añadir el gráfico
        doc.addImage(imgData, 'PNG', margin, currentY, imgWidth, imgHeight);
        currentY += imgHeight + 10;

        // Ahora procesamos cada pago individualmente
        return processPaymentDetails(doc, paymentItems, pageWidth, pageHeight, margin, currentY);
      });
    }).then(() => {
      // Guardar el PDF
      doc.save('Reporte_Pagos_Gimnasio_Dofit.pdf');
      
      // Restaurar el estado original de la página
      restorePageState(currentPageState, paginationControls, paymentItems);
      
      // Eliminar mensaje de carga
      document.body.removeChild(loadingMessage);
    }).catch(error => {
      console.error('Error al generar el PDF:', error);
      alert('Hubo un error al generar el PDF. Por favor, intente nuevamente.');
      
      // Restaurar el estado original de la página
      restorePageState(currentPageState, paginationControls, paymentItems);
      
      // Eliminar mensaje de carga
      document.body.removeChild(loadingMessage);
    });
  }, 500); // Dar tiempo para que el DOM se actualice
}

// Función para procesar los detalles de pago uno por uno
function processPaymentDetails(doc, paymentItems, pageWidth, pageHeight, margin, startY) {
  return new Promise(async (resolve) => {
    let currentY = startY;
    
    // Añadir título de detalles de pagos
    if (currentY + 10 > pageHeight - margin) {
      doc.addPage();
      currentY = margin;
    }

    doc.setFontSize(16);
    doc.text('Detalles de Pagos', margin, currentY);
    currentY += 10;
    
    // Procesar cada pago individualmente
    for (let i = 0; i < paymentItems.length; i++) {
      const paymentItem = paymentItems[i];
      
      try {
        // Capturar solo este elemento de pago
        const canvas = await html2canvas(paymentItem, {
          scale: 2,
          useCORS: true,
          logging: false,
          allowTaint: true,
          backgroundColor: '#ffffff'
        });
        
        const imgData = canvas.toDataURL('image/png');
        const imgWidth = pageWidth - margin * 2;
        const imgHeight = (canvas.height * imgWidth) / canvas.width;

        // Verificar si hay espacio suficiente en la página actual
        if (currentY + imgHeight > pageHeight - margin) {
          doc.addPage();
          currentY = margin;
        }

        // Añadir el pago al PDF
        doc.addImage(imgData, 'PNG', margin, currentY, imgWidth, imgHeight);
        currentY += imgHeight + 5;
        
        // Añadir un separador entre pagos
        if (i < paymentItems.length - 1) {
          doc.setDrawColor(200, 200, 200);
          doc.line(margin, currentY, pageWidth - margin, currentY);
          currentY += 5;
        }
      } catch (error) {
        console.error(`Error al procesar el pago ${i + 1}:`, error);
        // Continuar con el siguiente pago
      }
    }
    
    resolve();
  });
}

// Función para guardar el estado actual de la página
function getCurrentPageState() {
  return {
    scrollPosition: window.scrollY,
    currentPage: window.currentPage || 1
  };
}

// Función para restaurar el estado original de la página
function restorePageState(state, paginationControls, paymentItems) {
  // Restaurar controles de paginación
  paginationControls.forEach(control => {
    control.style.display = '';
  });
  
  // Restaurar visibilidad de los elementos de pago
  paymentItems.forEach(item => {
    item.style.display = 'none';
  });
  
  // Restaurar la paginación
  if (typeof goToPage === 'function') {
    goToPage(state.currentPage);
  }
  
  // Restaurar la posición de desplazamiento
  window.scrollTo(0, state.scrollPosition);
}

// Asegúrate de agregar el event listener para el botón de descarga
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('download-pdf').addEventListener('click', generatePDF);
});