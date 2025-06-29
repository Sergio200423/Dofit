document.addEventListener("DOMContentLoaded", () => {
  console.log("[DEBUG] Sistema de pagos cargado")

  // Variables globales
  let cart = []
  let products = []
  let memberships = []
  let discountPercentage = 0

  // Elementos del DOM
  const productsGrid = document.getElementById("products-grid")
  const membershipsGrid = document.getElementById("memberships-grid")
  const cartItems = document.getElementById("cart-items")
  const subtotalElement = document.getElementById("subtotal")
  const totalElement = document.getElementById("total")
  const discountInput = document.getElementById("discount")
  const checkoutBtn = document.getElementById("checkout-btn")
  const clearCartBtn = document.getElementById("clear-cart-btn")
  const productSearch = document.getElementById("product-search")
  const membershipSearch = document.getElementById("membership-search")

  // Modales
  const checkoutModal = document.getElementById("checkout-modal")
  const successModal = document.getElementById("success-modal")
  const modalItems = document.getElementById("modal-items")
  const modalSubtotal = document.getElementById("modal-subtotal")
  const modalDiscount = document.getElementById("modal-discount")
  const modalTotal = document.getElementById("modal-total")

  // Inicialización
  initializeTabs()
  loadProducts()
  loadMemberships()
  attachEventListeners()

  // Funciones de inicialización
  function initializeTabs() {
    const tabBtns = document.querySelectorAll(".tab-btn")
    const tabContents = document.querySelectorAll(".tab-content")

    tabBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        // Remover active de todos
        tabBtns.forEach((b) => b.classList.remove("active"))
        tabContents.forEach((c) => c.classList.remove("active"))

        // Activar seleccionado
        btn.classList.add("active")
        const tabId = btn.dataset.tab
        document.getElementById(`${tabId}-tab`).classList.add("active")
      })
    })
  }

  function attachEventListeners() {
    // Descuento
    discountInput.addEventListener("change", updateDiscount)

    // Botones del carrito
    checkoutBtn.addEventListener("click", showCheckoutModal)
    clearCartBtn.addEventListener("click", clearCart)

    // Búsqueda
    productSearch.addEventListener("input", searchProducts)
    membershipSearch.addEventListener("input", searchMemberships)

    // Modal
    document.getElementById("cancel-checkout").addEventListener("click", closeModals)
    document.getElementById("confirm-checkout").addEventListener("click", processPayment)
    document.getElementById("new-sale-btn").addEventListener("click", newSale)

    // Cerrar modales
    document.querySelectorAll(".close-modal").forEach((btn) => {
      btn.addEventListener("click", closeModals)
    })
  }

  // Cargar productos
  async function loadProducts() {
    try {
      const response = await fetch("/pagos/api/productos/", {
        headers: { "X-Requested-With": "XMLHttpRequest" },
      })
      const data = await response.json()

      products = data.productos || []
      renderProducts(products)
    } catch (error) {
      console.error("Error cargando productos:", error)
      productsGrid.innerHTML = '<p class="text-danger">Error al cargar productos</p>'
    }
  }

  // Cargar membresías
  async function loadMemberships() {
    try {
      const response = await fetch("/pagos/api/membresias/", {
        headers: { "X-Requested-With": "XMLHttpRequest" },
      })
      const data = await response.json()

      memberships = data.membresias || []
      renderMemberships(memberships)
    } catch (error) {
      console.error("Error cargando membresías:", error)
      membershipsGrid.innerHTML = '<p class="text-danger">Error al cargar membresías</p>'
    }
  }

  // Renderizar productos
  function renderProducts(productsToShow) {
    if (!productsToShow.length) {
      productsGrid.innerHTML = '<p class="text-muted">No hay productos disponibles</p>'
      return
    }

    productsGrid.innerHTML = productsToShow
      .map(
        (product) => `
            <div class="product-card" onclick="addToCart(${product.id_producto}, 'product')">
                <div class="product-image">
                    <img src="${product.imagen || "/static/img/placeholder.jpg"}" 
                         alt="${product.nombre_producto}"
                         onerror="this.src='/static/img/placeholder.jpg'">
                </div>
                <div class="product-info">
                    <div class="product-name">${product.nombre_producto}</div>
                    <div class="product-price">C$${Number(product.precio).toFixed(2)}</div>
                    <div class="product-stock">Stock: ${product.existencia}</div>
                </div>
            </div>
        `,
      )
      .join("")
  }

  // Renderizar membresías
  function renderMemberships(membershipsToShow) {
    if (!membershipsToShow.length) {
      membershipsGrid.innerHTML = '<p class="text-muted">No hay membresías disponibles</p>'
      return
    }

    membershipsGrid.innerHTML = membershipsToShow
      .map(
        (membership) => `
            <div class="membership-card" onclick="addToCart(${membership.id_membresia}, 'membership')">
                <div class="membership-header">
                    <div class="membership-name">${membership.nombreMembresia}</div>
                    <div class="membership-price">C$${Number(membership.precio).toFixed(2)}</div>
                    <div class="membership-duration">${membership.duracionDias} días</div>
                </div>
                <div class="membership-features">
                    <div class="membership-feature">
                        <i class="fas fa-check"></i>
                        Acceso completo al gimnasio
                    </div>
                    <div class="membership-feature">
                        <i class="fas fa-check"></i>
                        Uso de todas las máquinas
                    </div>
                    <div class="membership-feature">
                        <i class="fas fa-check"></i>
                        Asesoría personalizada
                    </div>
                </div>
            </div>
        `,
      )
      .join("")
  }

  // Añadir al carrito
  window.addToCart = (id, type) => {
    let item

    if (type === "product") {
      item = products.find((p) => p.id_producto === id)
      if (!item) return

      // Verificar stock
      const existingItem = cart.find((c) => c.id === id && c.type === type)
      const currentQuantity = existingItem ? existingItem.quantity : 0

      if (currentQuantity >= item.existencia) {
        alert("Stock insuficiente")
        return
      }

      if (existingItem) {
        existingItem.quantity++
      } else {
        cart.push({
          id: item.id_producto,
          name: item.nombre_producto,
          price: Number(item.precio),
          image: item.imagen,
          quantity: 1,
          stock: item.existencia,
          type: "product",
        })
      }
    } else if (type === "membership") {
      // Solo permitir una membresía
      if (cart.some((c) => c.type === "membership")) {
        alert("Solo puedes agregar una membresía por compra")
        return
      }

      item = memberships.find((m) => m.id_membresia === id)
      if (!item) return

      cart.push({
        id: item.id_membresia,
        name: item.nombreMembresia,
        price: Number(item.precio),
        quantity: 1,
        duration: `${item.duracionDias} días`,
        type: "membership",
      })
    }

    updateCart()
  }

  // Actualizar carrito
  function updateCart() {
    if (cart.length === 0) {
      cartItems.innerHTML = `
                <div class="empty-cart">
                    <i class="fas fa-shopping-cart"></i>
                    <p>El carrito está vacío</p>
                    <small>Añade productos o membresías para comenzar</small>
                </div>
            `
      checkoutBtn.disabled = true
      clearCartBtn.disabled = true
    } else {
      cartItems.innerHTML = cart
        .map(
          (item) => `
                <div class="cart-item">
                    <div class="cart-item-image">
                        ${
                          item.type === "product"
                            ? `<img src="${item.image || "/static/img/placeholder.jpg"}" alt="${item.name}">`
                            : `<i class="fas fa-id-card" style="font-size: 24px; color: var(--primary-blue);"></i>`
                        }
                    </div>
                    <div class="cart-item-details">
                        <div class="cart-item-name">${item.name}</div>
                        <div class="cart-item-price">
                            C$${item.price.toFixed(2)}
                            ${item.duration ? `(${item.duration})` : ""}
                        </div>
                    </div>
                    <div class="cart-item-actions">
                        <div class="quantity-control">
                            <button class="quantity-btn" onclick="changeQuantity(${item.id}, '${item.type}', -1)">-</button>
                            <input type="number" class="quantity-input" value="${item.quantity}" 
                                   onchange="setQuantity(${item.id}, '${item.type}', this.value)" min="1">
                            <button class="quantity-btn" onclick="changeQuantity(${item.id}, '${item.type}', 1)">+</button>
                        </div>
                        <div class="remove-item" onclick="removeFromCart(${item.id}, '${item.type}')">
                            <i class="fas fa-trash"></i>
                        </div>
                    </div>
                </div>
            `,
        )
        .join("")

      checkoutBtn.disabled = false
      clearCartBtn.disabled = false
    }

    updateTotals()
  }

  // Cambiar cantidad
  window.changeQuantity = (id, type, change) => {
    const item = cart.find((c) => c.id === id && c.type === type)
    if (!item) return

    const newQuantity = item.quantity + change

    if (newQuantity < 1) return

    if (type === "product" && newQuantity > item.stock) {
      alert("Stock insuficiente")
      return
    }

    if (type === "membership" && newQuantity > 1) {
      alert("Solo puedes comprar una membresía")
      return
    }

    item.quantity = newQuantity
    updateCart()
  }

  // Establecer cantidad
  window.setQuantity = (id, type, quantity) => {
    const item = cart.find((c) => c.id === id && c.type === type)
    if (!item) return

    const newQuantity = Number.parseInt(quantity)

    if (newQuantity < 1) {
      updateCart()
      return
    }

    if (type === "product" && newQuantity > item.stock) {
      alert("Stock insuficiente")
      updateCart()
      return
    }

    if (type === "membership" && newQuantity > 1) {
      alert("Solo puedes comprar una membresía")
      updateCart()
      return
    }

    item.quantity = newQuantity
    updateTotals()
  }

  // Remover del carrito
  window.removeFromCart = (id, type) => {
    cart = cart.filter((item) => !(item.id === id && item.type === type))
    updateCart()
  }

  // Actualizar totales
  function updateTotals() {
    const subtotal = cart.reduce((total, item) => total + item.price * item.quantity, 0)
    const discount = (subtotal * discountPercentage) / 100
    const total = subtotal - discount

    subtotalElement.textContent = `C$${subtotal.toFixed(2)}`
    totalElement.textContent = `C$${total.toFixed(2)}`
  }

  // Actualizar descuento
  function updateDiscount() {
    const value = Number.parseInt(discountInput.value) || 0
    discountPercentage = Math.max(0, Math.min(100, value))
    discountInput.value = discountPercentage
    updateTotals()
  }

  // Limpiar carrito
  function clearCart() {
    cart = []
    discountPercentage = 0
    discountInput.value = 0
    updateCart()
  }

  // Buscar productos
  function searchProducts() {
    const term = productSearch.value.toLowerCase()
    const filtered = products.filter((p) => p.nombre_producto.toLowerCase().includes(term))
    renderProducts(filtered)
  }

  // Buscar membresías
  function searchMemberships() {
    const term = membershipSearch.value.toLowerCase()
    const filtered = memberships.filter((m) => m.nombreMembresia.toLowerCase().includes(term))
    renderMemberships(filtered)
  }

  // Mostrar modal de checkout
  function showCheckoutModal() {
    if (cart.length === 0) return

    // Llenar items del modal
    modalItems.innerHTML = cart
      .map(
        (item) => `
            <div class="summary-item">
                <span class="summary-item-name">${item.name}</span>
                <span class="summary-item-quantity">x${item.quantity}</span>
                <span class="summary-item-price">C$${(item.price * item.quantity).toFixed(2)}</span>
            </div>
        `,
      )
      .join("")

    // Calcular totales
    const subtotal = cart.reduce((total, item) => total + item.price * item.quantity, 0)
    const discount = (subtotal * discountPercentage) / 100
    const total = subtotal - discount

    modalSubtotal.textContent = `C$${subtotal.toFixed(2)}`
    modalDiscount.textContent = `C$${discount.toFixed(2)}`
    modalTotal.textContent = `C$${total.toFixed(2)}`

    checkoutModal.style.display = "flex"
  }

  // Procesar pago - MEJORADO CON MEJOR MANEJO DE ERRORES
  async function processPayment() {
    const confirmBtn = document.getElementById("confirm-checkout")
    const originalText = confirmBtn.innerHTML

    try {
      // Mostrar estado de carga
      confirmBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Procesando...'
      confirmBtn.disabled = true

      const productos = cart
        .filter((item) => item.type === "product")
        .map((item) => ({
          id: item.id,
          quantity: item.quantity,
          name: item.name,
          price: item.price,
        }))

      const membresias = cart
        .filter((item) => item.type === "membership")
        .map((item) => ({
          id: item.id,
          quantity: item.quantity,
          name: item.name,
          price: item.price,
        }))

      const payload = {
        productos,
        membresias,
        descuento: discountPercentage,
      }

      console.log("Enviando payload:", payload)

      const response = await fetch("/pagos/realizar_pago/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": getCsrfToken(),
        },
        body: JSON.stringify(payload),
      })

      const data = await response.json()
      console.log("Respuesta del servidor:", data)

      if (data.success) {
        closeModals()
        showSuccessModal()
      } else {
        alert(`Error: ${data.error}`)
      }
    } catch (error) {
      console.error("Error procesando pago:", error)
      alert("Error al procesar el pago. Por favor, intenta de nuevo.")
    } finally {
      // Restaurar botón
      confirmBtn.innerHTML = originalText
      confirmBtn.disabled = false
    }
  }

  // Función para obtener CSRF token
  function getCsrfToken() {
    const cookies = document.cookie.split(";")
    for (const cookie of cookies) {
      const [name, value] = cookie.trim().split("=")
      if (name === "csrftoken") {
        return value
      }
    }
    // Fallback: buscar en meta tag
    const csrfMeta = document.querySelector('meta[name="csrf-token"]')
    return csrfMeta ? csrfMeta.getAttribute("content") : ""
  }

  // Mostrar modal de éxito
  function showSuccessModal() {
    successModal.style.display = "flex"
  }

  // Cerrar modales
  function closeModals() {
    checkoutModal.style.display = "none"
    successModal.style.display = "none"
  }

  // Nueva venta
  function newSale() {
    clearCart()
    closeModals()
    loadProducts() // Recargar para actualizar stock
  }
})
