// filtrarProducto.js - Actualizado para el nuevo diseño
document.addEventListener("DOMContentLoaded", () => {
  console.log("[DEBUG] filtrarProducto.js cargado correctamente")
  const form = document.getElementById("filtro-productos-form")
  const nombreInput = document.getElementById("nombre")
  const tipoCheckboxes = document.querySelectorAll('input[name="tipo"]')
  const estadoCheckboxes = document.querySelectorAll('input[name="estado"]')
  const tbody = document.getElementById("lista-productos")

  // Contadores de pills
  const contadorBarraEnergetica = document
    .querySelector("#tipoBarraEnergetica")
    ?.parentElement.querySelector(".pill-count")
  const contadorProteina = document.querySelector("#tipoProteina")?.parentElement.querySelector(".pill-count")
  const contadorVitaminas = document.querySelector("#tipoVitaminas")?.parentElement.querySelector(".pill-count")
  const contadorSuplementos = document.querySelector("#tipoSuplementos")?.parentElement.querySelector(".pill-count")
  const contadorBebidas = document.querySelector("#tipoBebidas")?.parentElement.querySelector(".pill-count")
  const contadorCaramelos = document.querySelector("#tipoCaramelos")?.parentElement.querySelector(".pill-count")
  const contadorDisponible = document.querySelector("#estadoDisponible")?.parentElement.querySelector(".pill-count")
  const contadorAgotado = document.querySelector("#estadoAgotado")?.parentElement.querySelector(".pill-count")

  function attachListeners() {
    nombreInput && nombreInput.addEventListener("input", filtrarProductos)
    tipoCheckboxes.forEach((cb) =>
      cb.addEventListener("change", () => {
        toggleActivePill(cb)
        filtrarProductos()
      }),
    )
    estadoCheckboxes.forEach((cb) =>
      cb.addEventListener("change", () => {
        toggleActivePill(cb)
        filtrarProductos()
      }),
    )
    if (form) {
      form.addEventListener("submit", (e) => {
        e.preventDefault()
        filtrarProductos()
      })
    }
  }

  function toggleActivePill(checkbox) {
    const label = checkbox.parentElement
    if (checkbox.checked) {
      label.classList.add("active")
    } else {
      label.classList.remove("active")
    }
  }

  function getSelectedValues(nodelist) {
    return Array.from(nodelist)
      .filter((cb) => cb.checked)
      .map((cb) => cb.value)
  }

  function filtrarProductos() {
    const tipos = getSelectedValues(tipoCheckboxes)
    const estados = getSelectedValues(estadoCheckboxes)
    const nombre = nombreInput ? nombreInput.value : ""

    console.log("[DEBUG] Filtros enviados:", { tipos, estados, nombre })

    fetch("/productos/filtrar/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({
        tipo: tipos,
        estado: estados,
        nombre: nombre,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("[DEBUG] Respuesta de filtrar_producto:", data)
        actualizarTablaProductos(data.productos)
        actualizarContadores(data)
      })
      .catch((error) => {
        console.error("Error al filtrar productos:", error)
      })
  }

  function actualizarTablaProductos(productos) {
    if (!tbody) return

    tbody.innerHTML = ""

    if (!productos || productos.length === 0) {
      tbody.innerHTML = `<tr><td colspan="8" class="empty-state"><p>No hay productos registrados</p></td></tr>`
      return
    }

    productos.forEach((producto) => {
      let estadoVisual = ""
      let estadoBadgeClass = ""
      let estadoTexto = ""

      if (producto.existencia === 0) {
        estadoVisual = "agotado"
        estadoBadgeClass = "state-agotado"
        estadoTexto = "AGOTADO"
      } else if (producto.existencia < 10) {
        estadoVisual = "pocas_unidades"
        estadoBadgeClass = "state-pocas"
        estadoTexto = "POCAS UNIDADES"
      } else {
        estadoVisual = "disponible"
        estadoBadgeClass = "state-disponible"
        estadoTexto = "DISPONIBLE"
      }

      const tr = document.createElement("tr")
      tr.setAttribute("data-producto-id", producto.id_producto)
      tr.innerHTML = `
        <td class="product-image-cell">
          <div class="product-image">
            ${
              producto.imagen
                ? `<img src="${producto.imagen}" alt="${producto.nombre_producto}">`
                : `<img src="/static/img/placeholder.jpg" alt="Sin imagen">`
            }
          </div>
        </td>
        <td class="product-name">${producto.nombre_producto}</td>
        <td class="product-price">$${producto.precio}</td>
        <td class="product-description">${producto.descripcion ? producto.descripcion.substring(0, 50) : ""}</td>
        <td class="product-quantity">${producto.existencia} unidades</td>
        <td class="product-type">${producto.tipo}</td>
        <td class="product-state">
          <span class="state-badge ${estadoBadgeClass}">${estadoTexto}</span>
        </td>
        <td class="product-actions">
          <button class="action-btn editar-producto-btn" data-id="${producto.id_producto}">
            <i class="fas fa-edit"></i> Editar
          </button>
        </td>
      `
      tbody.appendChild(tr)
    })

    // Actualizar event listeners para los nuevos botones de editar
    if (window.actualizarBotonesEditar) {
      window.actualizarBotonesEditar()
    }
  }

  function actualizarContadores(data) {
    if (contadorBarraEnergetica) contadorBarraEnergetica.textContent = data.barra_energetica_count ?? 0
    if (contadorProteina) contadorProteina.textContent = data.tipo_counts?.Proteina ?? 0
    if (contadorVitaminas) contadorVitaminas.textContent = data.tipo_counts?.Vitaminas ?? 0
    if (contadorSuplementos) contadorSuplementos.textContent = data.tipo_counts?.Suplementos ?? 0
    if (contadorBebidas) contadorBebidas.textContent = data.tipo_counts?.Bebidas ?? 0
    if (contadorCaramelos) contadorCaramelos.textContent = data.tipo_counts?.Caramelos ?? 0
    if (contadorDisponible) contadorDisponible.textContent = data.estado_counts?.disponible ?? 0
    if (contadorAgotado) contadorAgotado.textContent = data.estado_counts?.agotado ?? 0
  }

  function getCookie(name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";")
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim()
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
          break
        }
      }
    }
    return cookieValue
  }

  attachListeners()

  // Inicializar estado visual de los pills
  tipoCheckboxes.forEach((cb) => toggleActivePill(cb))
  estadoCheckboxes.forEach((cb) => toggleActivePill(cb))
})
