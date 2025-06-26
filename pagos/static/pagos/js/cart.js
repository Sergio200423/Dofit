console.log('[DEBUG] cart.js cargado correctamente');

document.addEventListener("DOMContentLoaded", () => {
    // Datos de productos (simulados)
    const products = []
  
    // Datos de membresías (simulados)
    const memberships = [];
  
    // Variables globales
    let cart = []
    let discountPercentage = 0
  
    // Elementos del DOM
    const productGrid = document.getElementById("product-grid")
    const cartItems = document.getElementById("cart-items")
    const subtotalElement = document.getElementById("subtotal")
    const totalElement = document.getElementById("total")
    const discountInput = document.getElementById("discount")
    const checkoutBtn = document.getElementById("checkout-btn")
    const clearCartBtn = document.getElementById("clear-cart-btn")
    const productSearch = document.getElementById("product-search")
    const searchBtn = document.getElementById("search-btn")
    const newSaleBtn = document.getElementById("new-sale-btn")
  
    // Elementos del modal
    const checkoutModal = document.getElementById("checkout-modal")
    const confirmationModal = document.getElementById("confirmation-modal")
    const modalItems = document.getElementById("modal-items")
    const modalSubtotal = document.getElementById("modal-subtotal")
    const modalDiscount = document.getElementById("modal-discount")
    const modalTotal = document.getElementById("modal-total")
    const cancelCheckout = document.getElementById("cancel-checkout")
    const confirmCheckout = document.getElementById("confirm-checkout")
    const closeModalButtons = document.querySelectorAll(".close-modal")
    // Corregido: solo asignar si existen
    const printReceipt = document.getElementById("print-receipt")
    const newPurchase = document.getElementById("new-purchase")
  
    // Cargar productos
    function loadProducts(productsToShow = products) {
      productGrid.innerHTML = ""

      productsToShow.forEach((product) => {
        const productCard = document.createElement("div")
        productCard.className = "product-card"
        // Si no hay imagen, usar dofit.jpg
        const imageSrc = product.image ? product.image : "/static/img/dofit.jpg";
        productCard.innerHTML = `
                  <div class="product-image">
                      <img src="${imageSrc}" alt="${product.name}" onerror="this.src='/static/img/dofit.jpg'">
                  </div>
                  <div class="product-info">
                      <div class="product-name">${product.name}</div>
                      <div class="product-price">C$${product.price.toFixed(2)}</div>
                      <div class="product-stock">Stock: ${product.stock}</div>
                  </div>
              `

        productCard.addEventListener("click", () => addToCart(product))
        productGrid.appendChild(productCard)
      })
    }
  
    // Cargar membresías
    function loadMemberships(membershipsToShow = memberships) {
      const membershipGrid = document.getElementById("membership-grid")
      membershipGrid.innerHTML = ""
  
      membershipsToShow.forEach((membership) => {
        const membershipCard = document.createElement("div")
        membershipCard.className = "membership-card"

        let featuresHTML = ""
        membership.features.forEach((feature) => {
          featuresHTML += `<div class="membership-feature"><i class="fas fa-check"></i>${feature}</div>`
        })

        membershipCard.innerHTML = `
          <div class="membership-header">
            <div class="membership-name">${membership.name}</div>
            <div class="membership-price">C$${membership.price.toFixed(2)}</div>
            <div class="membership-duration">${membership.duration}</div>
          </div>
          <div class="membership-features">
            ${featuresHTML}
          </div>
          <div class="membership-footer">
            <button class="primary-btn add-membership-btn">Añadir al carrito</button>
          </div>
        `

        // Permitir agregar al carrito haciendo click en cualquier parte de la tarjeta
        membershipCard.addEventListener("click", () => addToCart(membership))
        // Prevenir doble acción si se hace click en el botón
        membershipCard.querySelector(".add-membership-btn").addEventListener("click", (e) => {
          e.stopPropagation();
          addToCart(membership);
        })
        membershipGrid.appendChild(membershipCard)
      })
    }
  
    // Añadir producto al carrito
    function addToCart(item) {
      // Si el item es membresía y ya hay una membresía en el carrito, no permitir agregar otra
      if (item.type === "membership") {
        const yaHayMembresia = cart.some((cartItem) => cartItem.type === "membership");
        if (yaHayMembresia) {
          alert("Solo puedes agregar una membresía al carrito por cliente.");
          return;
        }
      }
      const existingItem = cart.find((cartItem) => cartItem.id === item.id && cartItem.type === item.type)

      if (existingItem) {
        if (item.type === "product") {
          if (existingItem.quantity < item.stock) {
            existingItem.quantity++
            updateCart()
          } else {
            alert("No hay suficiente stock disponible")
          }
        } else {
          existingItem.quantity++
          updateCart()
        }
      } else {
        // Solo agrega duration y features si existen (para membresías)
        const cartItem = {
          id: item.id,
          name: item.name,
          price: item.price,
          image: item.image,
          quantity: 1,
          stock: item.stock,
          type: item.type
        };
        if (item.duration) cartItem.duration = item.duration;
        if (item.features) cartItem.features = item.features;
        cart.push(cartItem);
        updateCart()
      }
    }
  
    // Actualizar carrito
    function updateCart() {
      if (cart.length === 0) {
        cartItems.innerHTML = `
        <div class="empty-cart">
          <i class="fas fa-shopping-cart"></i>
          <p>El carrito está vacío</p>
        </div>
      `
        checkoutBtn.disabled = true
        clearCartBtn.disabled = true
        document.getElementById("cart-categories").style.display = "none"
      } else {
        cartItems.innerHTML = ""
  
        cart.forEach((item) => {
          const cartItem = document.createElement("div")
          cartItem.className = "cart-item"
  
          // Determinar el tipo de badge
          const typeBadge =
            item.type === "product"
              ? '<span class="item-type product">Producto</span>'
              : '<span class="item-type membership">Membresía</span>'
  
          // Mostrar imagen solo para productos, para membresía mostrar ícono
          let imageHTML = "";
          if (item.type === "product") {
            imageHTML = `<img src="${item.image || "/static/img/placeholder.jpg"}" alt="${item.name}" onerror="this.src='/static/img/placeholder.jpg'">`;
          } else {
            imageHTML = `<div class="membership-icon"><i class="fas fa-id-card"></i></div>`;
          }
  
          cartItem.innerHTML = `
          <div class="cart-item-image">
            ${imageHTML}
          </div>
          <div class="cart-item-details">
            <div class="cart-item-name">${item.name} ${typeBadge}</div>
            <div class="cart-item-price">C$${item.price.toFixed(2)} ${item.type === "membership" ? `(${item.duration})` : ""}</div>
          </div>
          <div class="cart-item-actions">
            <div class="quantity-control">
              <button class="quantity-btn minus" data-id="${item.id}" data-type="${item.type}">-</button>
              <input type="number" class="quantity-input" value="${item.quantity}" min="1" max="${item.stock || 99}" data-id="${item.id}" data-type="${item.type}">
              <button class="quantity-btn plus" data-id="${item.id}" data-type="${item.type}">+</button>
            </div>
            <div class="remove-item" data-id="${item.id}" data-type="${item.type}">
              <i class="fas fa-trash"></i>
            </div>
          </div>
        `
  
          cartItems.appendChild(cartItem)
        })
  
        // Añadir event listeners a los botones de cantidad y eliminar
        document.querySelectorAll(".quantity-btn.minus").forEach((btn) => {
          btn.addEventListener("click", () => decreaseQuantity(Number.parseInt(btn.dataset.id), btn.dataset.type))
        })
  
        document.querySelectorAll(".quantity-btn.plus").forEach((btn) => {
          btn.addEventListener("click", () => increaseQuantity(Number.parseInt(btn.dataset.id), btn.dataset.type))
        })
  
        document.querySelectorAll(".quantity-input").forEach((input) => {
          input.addEventListener("change", (e) =>
            updateQuantity(Number.parseInt(input.dataset.id), Number.parseInt(e.target.value), input.dataset.type),
          )
        })
  
        document.querySelectorAll(".remove-item").forEach((btn) => {
          btn.addEventListener("click", () => removeFromCart(Number.parseInt(btn.dataset.id), btn.dataset.type))
        })
  
        checkoutBtn.disabled = false
        clearCartBtn.disabled = false
  
        // Mostrar totales por categoría
        document.getElementById("cart-categories").style.display = "block"
      }
  
      updateTotals()
    }
  
    // Disminuir cantidad
    function decreaseQuantity(id, type) {
      const item = cart.find((item) => item.id === id && item.type === type)
      if (item && item.quantity > 1) {
        item.quantity--
        updateCart()
      }
    }
  
    // Aumentar cantidad
    function increaseQuantity(id, type) {
      const item = cart.find((item) => item.id === id && item.type === type)
      if (item) {
        if (item.type === "product" && item.quantity < item.stock) {
          item.quantity++
          updateCart()
        } else if (item.type === "membership") {
          item.quantity++
          updateCart()
        } else {
          alert("No hay suficiente stock disponible")
        }
      }
    }
  
    // Actualizar cantidad directamente
    function updateQuantity(id, quantity, type) {
      const item = cart.find((item) => item.id === id && item.type === type)
      if (item) {
        if (item.type === "product" && quantity > item.stock) {
          alert("No hay suficiente stock disponible")
          updateCart() // Restaurar valor anterior
        } else if (quantity < 1) {
          updateCart() // Restaurar valor anterior
        } else {
          item.quantity = quantity
          updateTotals()
        }
      }
    }
  
    // Eliminar del carrito
    function removeFromCart(id, type) {
      cart = cart.filter((item) => !(item.id === id && item.type === type))
      updateCart()
    }
  
    // Actualizar totales
    function updateTotals() {
      const subtotal = cart.reduce((total, item) => total + item.price * item.quantity, 0)
      const discount = (subtotal * discountPercentage) / 100
      const total = subtotal - discount
  
      // Calcular totales por categoría
      const productsTotal = cart
        .filter((item) => item.type === "product")
        .reduce((total, item) => total + item.price * item.quantity, 0)
  
      const membershipsTotal = cart
        .filter((item) => item.type === "membership")
        .reduce((total, item) => total + item.price * item.quantity, 0)
  
      subtotalElement.textContent = `C$${subtotal.toFixed(2)}`
      totalElement.textContent = `C$${total.toFixed(2)}`
  
      // Actualizar totales por categoría
      document.getElementById("products-total").textContent = `C$${productsTotal.toFixed(2)}`
      document.getElementById("memberships-total").textContent = `C$${membershipsTotal.toFixed(2)}`
    }
  
    // Vaciar carrito
    function clearCart() {
      cart = []
      updateCart()
    }
  
    // Buscar productos
    function searchProducts() {
      const searchTerm = productSearch.value.toLowerCase().trim()
  
      if (searchTerm === "") {
        loadProducts()
        return
      }
  
      const filteredProducts = products.filter((product) => product.name.toLowerCase().includes(searchTerm))
  
      loadProducts(filteredProducts)
    }
  
    // Buscar membresías
    function searchMemberships() {
      const searchTerm = document.getElementById("membership-search").value.toLowerCase().trim()
  
      if (searchTerm === "") {
        loadMemberships()
        return
      }
  
      const filteredMemberships = memberships.filter(
        (membership) =>
          membership.name.toLowerCase().includes(searchTerm) ||
          membership.features.some((feature) => feature.toLowerCase().includes(searchTerm)),
      )
  
      loadMemberships(filteredMemberships)
    }
  
    // --- CLIENTES: cargar y buscar dinámicamente ---
    function cargarClientesSelector(clientes) {
      const clientSelect = document.getElementById("client-select");
      clientSelect.innerHTML = '<option value="">Seleccionar cliente</option>';
      clientes.forEach(cliente => {
        clientSelect.innerHTML += `<option value="${cliente.id_cliente}">${cliente.nombre_cliente}</option>`;
      });
    }


    // Llamar a la API de clientes al cargar la página
    function cargarClientesAPI() {
      fetch('/api/clientes/', { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
        .then(r => r.json())
        .then((data) => {
          if (data.clientes) cargarClientesSelector(data.clientes);
        });
    }


    // Cargar membresías desde la API
    function cargarMembresiasAPI() {
      console.log('[DEBUG] Ejecutando cargarMembresiasAPI()');
      fetch('/api/tipo_membresias/', {
        method: 'GET',
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('[DEBUG] Data recibida de /api/tipo_membresias/:', data);
        memberships.length = 0;
        if (data.membresias && data.membresias.length > 0) {
          data.membresias.forEach(m => {
            memberships.push({
              id: m.id_membresia,
              name: m.nombreMembresia,
              price: Number(m.precio),
              duration: m.duracionDias + ' días',
              features: m.features || [], // Si tu API devuelve features
              type: 'membership',
              image: m.imagen || '/static/img/placeholder.jpg',
            });
          });
          loadMemberships(memberships);
        } else {
          document.getElementById('membership-grid').innerHTML = '<p class="text-muted">No hay membresías disponibles.</p>';
        }
      })
      .catch(error => {
        document.getElementById('membership-grid').innerHTML = '<p class="text-danger">No se pudieron cargar las membresías. Intenta más tarde.</p>';
        console.error('[DEBUG] Error al obtener la lista de membresías:', error);
      });
    }

    // Mostrar modal de checkout
    function showCheckoutModal() {
      modalItems.innerHTML = ""
  
      cart.forEach((item) => {
        const summaryItem = document.createElement("div")
        summaryItem.className = "summary-item"
        summaryItem.innerHTML = `
                  <span class="summary-item-name">${item.name}</span>
                  <span class="summary-item-quantity">x${item.quantity}</span>
                  <span class="summary-item-price">C$${(item.price * item.quantity).toFixed(2)}</span>
              `
  
        modalItems.appendChild(summaryItem)
      })
  
      const subtotal = cart.reduce((total, item) => total + item.price * item.quantity, 0)
      const discount = (subtotal * discountPercentage) / 100
      const total = subtotal - discount
  
      modalSubtotal.textContent = `C$${subtotal.toFixed(2)}`
      modalDiscount.textContent = `C$${discount.toFixed(2)}`
      modalTotal.textContent = `C$${total.toFixed(2)}`
  
      checkoutModal.style.display = "flex"
    }
  
    // Cerrar modales
    function closeModals() {
      checkoutModal.style.display = "none"
      confirmationModal.style.display = "none"
    }
  
    // Nueva venta
    function startNewSale() {
      clearCart()
      closeModals()
      discountInput.value = 0
      discountPercentage = 0
      updateTotals()
    }
  
    // Cargar productos desde la API para pagos.html
    function cargarProductosPagos() {
      console.log('[DEBUG] Ejecutando cargarProductosPagos()');
      fetch('/api/productos/', {
          method: 'GET',
          headers: {
              'X-Requested-With': 'XMLHttpRequest'
          }
      })
      .then(response => {
          console.log('[DEBUG] Respuesta de /api/productos/:', response);
          if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
      })
      .then(data => {
          console.log('[DEBUG] Data recibida de /api/productos/:', data);
          const grid = document.getElementById('product-grid');
          grid.innerHTML = '';
          // ACTUALIZAR products global con los productos de la API
          products.length = 0;
          if (data.productos && data.productos.length > 0) {
              data.productos.forEach(producto => {
                  products.push({
                      id: producto.id_producto,
                      name: producto.nombre_producto,
                      price: Number(producto.precio),
                      image: producto.imagen || '/static/img/placeholder.jpg',
                      stock: producto.existencia,
                      type: 'product',
                  });
                  const card = document.createElement('div');
                  card.className = 'product-card';
                  card.innerHTML = `
                      <div class="product-img">
                          <img src="${producto.imagen || '/static/img/placeholder.jpg'}" alt="${producto.nombre_producto}" onerror="this.src='/static/img/placeholder.jpg'">
                      </div>
                      <div class="product-info">
                          <h4>${producto.nombre_producto}</h4>
                          <p class="product-type">${producto.tipo}</p>
                          <p class="product-price">C$${Number(producto.precio).toFixed(2)}</p>
                          <p class="product-stock">Stock: ${producto.existencia}</p>
                          <button class="add-to-cart-btn">
                              <i class="fas fa-cart-plus"></i> Agregar
                          </button>
                      </div>
                  `;
                  // Datos del producto para el carrito
                  const productData = {
                      id: producto.id_producto,
                      name: producto.nombre_producto,
                      price: Number(producto.precio),
                      image: producto.imagen || '/static/img/placeholder.jpg',
                      stock: producto.existencia,
                      type: 'product',
                  };
                  // Listener para toda la tarjeta
                  card.addEventListener('click', function() {
                      addToCart(productData);
                  });
                  // Listener solo para el botón, previene doble acción
                  card.querySelector('.add-to-cart-btn').addEventListener('click', function(event) {
                      event.stopPropagation();
                      addToCart(productData);
                  });
                  grid.appendChild(card);
              });
              console.log('[DEBUG] Productos renderizados en la grilla:', products.length);
          } else {
              grid.innerHTML = '<p class="text-muted">No hay productos disponibles.</p>';
              console.warn('[DEBUG] No hay productos disponibles en la API.');
          }
      })
      .catch(error => {
          const grid = document.getElementById('product-grid');
          grid.innerHTML = '<p class="text-danger">No se pudieron cargar los productos. Intenta más tarde.</p>';
          console.error('[DEBUG] Error al obtener la lista de productos:', error);
      });
    }
  
    // --- FINALIZAR COMPRA: Enviar datos al backend ---
    function realizarCompra() {
      const clientSelect = document.getElementById("client-select");
      const clienteId = clientSelect.value;
      if (!clienteId) {
        alert("Selecciona un cliente antes de finalizar la compra.");
        return;
      }
      if (cart.length === 0) {
        alert("El carrito está vacío.");
        return;
      }
      // Mensaje de depuración para membresías
      cart.forEach(item => {
        if (item.type === 'membership') {
          console.log('[DEBUG] Pago de membresía detectado:', item);
        }
      });
      // Preparar datos para el backend
      let productos = cart.filter(item => item.type === 'product').map(item => ({
        id: item.id,
        name: item.name,
        price: item.price,
        quantity: item.quantity,
        type: item.type,
      }));
      const membresias = cart.filter(item => item.type === 'membership').map(item => ({
        id: item.id,
        name: item.name,
        price: item.price,
        quantity: item.quantity,
        duration: item.duration,
        features: item.features,
        type: item.type,
      }));
      // Eliminar la lógica que forzaba membresías como productos
      const payload = {
        cliente_id: clienteId,
        productos: productos,
        membresias: membresias,
        descuento: discountPercentage,
        total: [...productos, ...membresias].reduce((acc, p) => acc + p.price * p.quantity, 0) * (1 - discountPercentage/100)
      };
      console.log('Payload a enviar:', payload); // <-- DEBUG
      fetch('/api/realizar_pago/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify(payload)
      })
      .then(r => r.json())
      .then(async data => {
        if (data.success) {
          // showConfirmationModal();
          // startNewSale(); // No cerrar el modal de confirmación automáticamente
          cargarProductosPagos(); // Refresca la grilla con el formato correcto
          // Redirigir a la página para que Django muestre el mensaje
          window.location.href = '/pagos/?success=1';
        } else {
          // Mostrar mensaje de error detallado del backend
          let errorMsg = data.error || JSON.stringify(data);
          alert('Error al registrar el pago: ' + errorMsg);
          console.error('[DEBUG] Error backend:', data);
        }
      })
      .catch(err => {
        alert('Error de red al registrar el pago.');
        console.error(err);
      });
    }

    // Event Listeners
    discountInput.addEventListener("change", function () {
      const value = Number.parseInt(this.value)
      if (isNaN(value) || value < 0) {
        this.value = 0
        discountPercentage = 0
      } else if (value > 100) {
        this.value = 100
        discountPercentage = 100
      } else {
        discountPercentage = value
      }
      updateTotals()
    })
  
    checkoutBtn.addEventListener("click", showCheckoutModal)
    clearCartBtn.addEventListener("click", clearCart)
    searchBtn.addEventListener("click", searchProducts)
    productSearch.addEventListener("keyup", (e) => {
      if (e.key === "Enter") {
        searchProducts()
      }
    })
  
    cancelCheckout.addEventListener("click", closeModals)
    confirmCheckout.addEventListener("click", realizarCompra)
  
    closeModalButtons.forEach((button) => {
      button.addEventListener("click", closeModals)
    })
  
    if (printReceipt) {
      printReceipt.addEventListener("click", () => {
        alert("Imprimiendo recibo...")
        // Aquí iría la lógica para imprimir el recibo
      })
    }

    if (newPurchase) {
      newPurchase.addEventListener("click", startNewSale)
    }
  
    // Event listeners para las pestañas
    document.querySelectorAll(".tab-btn").forEach((button) => {
      button.addEventListener("click", () => {
        // Remover clase active de todas las pestañas
        document.querySelectorAll(".tab-btn").forEach((btn) => {
          btn.classList.remove("active")
        })
  
        // Ocultar todos los contenidos de pestañas
        document.querySelectorAll(".tab-content").forEach((content) => {
          content.style.display = "none"
        })
  
        // Activar la pestaña seleccionada
        button.classList.add("active")
        const tabId = button.dataset.tab
        document.getElementById(`${tabId}-tab`).style.display = "block"
      })
    })
  
    // Event listener para búsqueda de membresías
    const membershipSearchBtn = document.getElementById("membership-search-btn");
    const membershipSearchInput = document.getElementById("membership-search");
    if (membershipSearchBtn) {
      membershipSearchBtn.addEventListener("click", searchMemberships);
    }
    if (membershipSearchInput) {
      membershipSearchInput.addEventListener("keyup", (e) => {
        if (e.key === "Enter") {
          searchMemberships();
        }
      });
    }
    // Mostrar pestaña de productos por defecto
    const productsTab = document.getElementById("products-tab");
    if (productsTab) {
      productsTab.style.display = "block";
    }
    // Inicializar
    cargarMembresiasAPI();
    loadMemberships(); // Se actualizará con la API
    updateCart();
    cargarClientesAPI();
    cargarProductosPagos();
  })
