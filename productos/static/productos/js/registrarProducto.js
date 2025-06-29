// Script para manejar el modal de registro/edición de productos
console.log("registrarProducto.js cargado correctamente")

document.addEventListener("DOMContentLoaded", () => {
  // Referencias a elementos del DOM
  const openModalBtn = document.getElementById("openModalBtn")
  const registroProductoModal = document.getElementById("registroProductoModal")
  const registroProductoForm = document.getElementById("registroProductoForm")
  const modalTitle = document.getElementById("registroProductoModalLabel")
  const submitBtn = registroProductoForm?.querySelector('button[type="submit"]')
  const imagenInput = document.getElementById("imagen")
  const imagenUploadArea = document.getElementById("imagenUploadArea")
  const imagenPreviewContainer = document.getElementById("imagenPreviewContainer")
  const imagenPreview = document.getElementById("imagenPreview")
  const eliminarImagen = document.getElementById("eliminarImagen")

  // Variables para controlar el modo (registro/edición)
  let isEditMode = false
  let editingProductId = null

  // Funciones para abrir el modal
  function openProductoModal(mode = "add", productData = null) {
    if (!registroProductoModal) return

    isEditMode = mode === "edit"
    editingProductId = productData?.id_producto || null

    // Cambiar título y botón según el modo
    if (isEditMode) {
      modalTitle.textContent = "Editar Producto"
      submitBtn.textContent = "Guardar Cambios"
      registroProductoForm.action = `/productos/editar/${editingProductId}/`
    } else {
      modalTitle.textContent = "Registrar Nuevo Producto"
      submitBtn.textContent = "Registrar"
      registroProductoForm.action = "/productos/registrar/"
    }

    // Limpiar formulario primero
    registroProductoForm.reset()
    limpiarVistaPrevia()

    // Si es modo edición, llenar los campos
    if (isEditMode && productData) {
      llenarFormulario(productData)
    }

    // Mostrar el modal
    const modalInstance = new window.bootstrap.Modal(registroProductoModal)
    modalInstance.show()
  }

  function llenarFormulario(productData) {
    // Llenar campos básicos
    document.getElementById("nombre_producto").value = productData.nombre_producto || ""
    document.getElementById("precio").value = productData.precio || ""
    document.getElementById("descripcion").value = productData.descripcion || ""
    document.getElementById("tipo").value = productData.tipo || ""
    document.getElementById("existencia").value = productData.existencia || ""

    // Fecha de ingreso (si existe)
    if (productData.fecha_ingreso) {
      document.getElementById("fecha_ingreso").value = productData.fecha_ingreso
    }

    // Mostrar imagen actual si existe
    if (productData.imagen_url) {
      imagenPreview.src = productData.imagen_url
      imagenPreviewContainer.style.display = "block"
      if (imagenUploadArea) {
        const textCenter = imagenUploadArea.querySelector(".text-center")
        if (textCenter) textCenter.style.display = "none"
      }
    }
  }

  function limpiarVistaPrevia() {
    if (imagenPreviewContainer) imagenPreviewContainer.style.display = "none"
    if (imagenUploadArea) {
      const textCenter = imagenUploadArea.querySelector(".text-center")
      if (textCenter) textCenter.style.display = "block"
    }
    if (imagenInput) imagenInput.value = ""
  }

  // Event listeners para abrir el modal (nuevo producto)
  if (openModalBtn) {
    openModalBtn.addEventListener("click", () => openProductoModal("add"))
  }

  // Event listeners para botones de editar
  function attachEditListeners() {
    const editBtns = document.querySelectorAll(".editar-producto-btn")
    editBtns.forEach((btn) => {
      btn.removeEventListener("click", handleEditClick)
      btn.addEventListener("click", handleEditClick)
    })
  }

  function handleEditClick(event) {
    event.preventDefault()
    event.stopPropagation()

    const productoId = this.getAttribute("data-id")
    console.log("Editando producto ID:", productoId)

    // Cargar datos del producto directamente sin mostrar alertas de error
    fetch(`/productos/obtener/${productoId}/`)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        return response.json()
      })
      .then((data) => {
        if (data.error) {
          console.error("Error del servidor:", data.error)
          return
        }
        console.log("Datos del producto cargados:", data)
        // Abrir modal en modo edición con los datos
        openProductoModal("edit", data)
      })
      .catch((error) => {
        console.error("Error al cargar los datos del producto:", error)
        // No mostrar alert, solo log en consola
      })
  }

  // Manejar la carga de imágenes
  if (imagenUploadArea) {
    imagenUploadArea.addEventListener("click", () => {
      if (imagenInput) imagenInput.click()
    })

    // Arrastrar y soltar imágenes
    imagenUploadArea.addEventListener("dragover", (e) => {
      e.preventDefault()
      imagenUploadArea.classList.add("border-primary")
    })

    imagenUploadArea.addEventListener("dragleave", () => {
      imagenUploadArea.classList.remove("border-primary")
    })

    imagenUploadArea.addEventListener("drop", (e) => {
      e.preventDefault()
      imagenUploadArea.classList.remove("border-primary")

      if (e.dataTransfer.files.length && imagenInput) {
        imagenInput.files = e.dataTransfer.files
        mostrarVistaPrevia()
      }
    })
  }

  // Mostrar vista previa de la imagen seleccionada
  if (imagenInput) {
    imagenInput.addEventListener("change", mostrarVistaPrevia)
  }

  function mostrarVistaPrevia() {
    if (imagenInput && imagenInput.files && imagenInput.files[0]) {
      const reader = new FileReader()

      reader.onload = (e) => {
        if (imagenPreview) imagenPreview.src = e.target.result
        if (imagenPreviewContainer) imagenPreviewContainer.style.display = "block"
        if (imagenUploadArea) {
          const textCenter = imagenUploadArea.querySelector(".text-center")
          if (textCenter) textCenter.style.display = "none"
        }
      }

      reader.readAsDataURL(imagenInput.files[0])
    }
  }

  // Eliminar imagen seleccionada
  if (eliminarImagen) {
    eliminarImagen.addEventListener("click", () => {
      limpiarVistaPrevia()
    })
  }

  // Validación y envío del formulario
  const alertMessage = document.getElementById("alert-message-productos")

  if (registroProductoForm) {
    registroProductoForm.addEventListener("submit", (e) => {
      e.preventDefault()

      // Validaciones
      const precio = document.getElementById("precio")
      if (precio && Number.parseFloat(precio.value) <= 0) {
        mostrarAlerta("El precio debe ser mayor que cero.", "error")
        return false
      }

      const existencia = document.getElementById("existencia")
      if (
        existencia &&
        (Number.parseInt(existencia.value) < 0 || !Number.isInteger(Number.parseFloat(existencia.value)))
      ) {
        mostrarAlerta("La existencia debe ser un número entero positivo.", "error")
        return false
      }

      // Preparar datos para envío
      const formData = new FormData(registroProductoForm)

      // Fecha actual si no se seleccionó (solo para nuevos productos)
      if (!isEditMode && !formData.get("fecha_ingreso")) {
        formData.set("fecha_ingreso", new Date().toISOString().slice(0, 10))
      }

      // Determinar URL y método
      const url = isEditMode ? `/productos/editar/${editingProductId}/` : "/productos/registrar/"

      fetch(url, {
        method: "POST",
        headers: {
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
        },
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.InformacionValida) {
            const mensaje = isEditMode
              ? data.message || "Producto actualizado exitosamente."
              : data.message || "Producto registrado exitosamente."

            mostrarAlerta(mensaje, "success")

            // Limpiar formulario
            registroProductoForm.reset()
            limpiarVistaPrevia()

            // Cerrar modal
            const modalInstance = window.bootstrap.Modal.getInstance(registroProductoModal)
            if (modalInstance) {
              modalInstance.hide()
            }

            // Recargar la página después de 1 segundo
            setTimeout(() => {
              location.reload()
            }, 1000)
          } else {
            mostrarAlerta(data.message || "Error al procesar la solicitud", "error")
          }
        })
        .catch((error) => {
          console.error("Error:", error)
          mostrarAlerta("Error en la operación: " + error, "error")
        })
    })
  }

  function mostrarAlerta(mensaje, tipo) {
    if (alertMessage) {
      alertMessage.style.display = "block"
      alertMessage.textContent = mensaje

      if (tipo === "success") {
        alertMessage.style.backgroundColor = "rgba(16, 185, 129, 0.1)"
        alertMessage.style.color = "#10b981"
        alertMessage.style.border = "1px solid #10b981"
      } else {
        alertMessage.style.backgroundColor = "rgba(239, 68, 68, 0.1)"
        alertMessage.style.color = "#ef4444"
        alertMessage.style.border = "1px solid #ef4444"
      }

      // Auto-ocultar después de 5 segundos
      setTimeout(() => {
        alertMessage.style.display = "none"
      }, 5000)
    }
  }

  // Inicializar event listeners para botones de editar
  attachEditListeners()

  // Exponer función globalmente para uso en filtros
  window.actualizarBotonesEditar = attachEditListeners
})
