// Script para manejar el modal de registro de productos

// DEBUG: Verificar si el script se está cargando
console.log('registrarProducto.js cargado correctamente');

document.addEventListener('DOMContentLoaded', function() {
    // Referencias a elementos del DOM para el registro de productos
    const openModalBtn = document.getElementById('openModalBtn');
    const registroProductoModal = document.getElementById('registroProductoModal');
    const imagenInput = document.getElementById('imagen');
    const imagenUploadArea = document.getElementById('imagenUploadArea');
    const imagenPreviewContainer = document.getElementById('imagenPreviewContainer');
    const imagenPreview = document.getElementById('imagenPreview');
    const eliminarImagen = document.getElementById('eliminarImagen');
    
    // Funciones para abrir y cerrar el modal de productos (accesibilidad con inert)
    function openProductoModal() {
        registroProductoModal.style.display = "block";
        document.body.style.overflow = "hidden"; // Prevenir scroll
        registroProductoModal.removeAttribute("inert");
    }

    function closeProductoModal() {
        registroProductoModal.style.display = "none";
        document.body.style.overflow = ""; // Restaurar scroll
        registroProductoModal.setAttribute("inert", "");
        if (registroProductoForm) registroProductoForm.reset();
        const alertMessage = document.getElementById('alert-message-productos');
        if (alertMessage) alertMessage.style.display = 'none';
    }

    // Event listeners para abrir/cerrar el modal
    if (openModalBtn && registroProductoModal) {
        openModalBtn.addEventListener('click', openProductoModal);
        // Cerrar con botón de Bootstrap
        const closeBtns = registroProductoModal.querySelectorAll('[data-bs-dismiss="modal"], .btn-close');
        closeBtns.forEach(btn => btn.addEventListener('click', closeProductoModal));
        // Cerrar al hacer clic fuera del contenido
        window.addEventListener('click', function(event) {
            if (event.target === registroProductoModal) {
                closeProductoModal();
            }
        });
    }
    
    // Eliminar cualquier manejo de 'inert' para el modal de productos
    // Solo dejar que Bootstrap maneje el modal
    
    // Manejar la carga de imágenes
    if (imagenUploadArea) {
        imagenUploadArea.addEventListener('click', function() {
            imagenInput.click();
        });
        
        // Arrastrar y soltar imágenes
        imagenUploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            imagenUploadArea.classList.add('border-primary');
        });
        
        imagenUploadArea.addEventListener('dragleave', function() {
            imagenUploadArea.classList.remove('border-primary');
        });
        
        imagenUploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            imagenUploadArea.classList.remove('border-primary');
            
            if (e.dataTransfer.files.length) {
                imagenInput.files = e.dataTransfer.files;
                mostrarVistaPrevia();
            }
        });
    }
    
    // Mostrar vista previa de la imagen seleccionada
    if (imagenInput) {
        imagenInput.addEventListener('change', mostrarVistaPrevia);
    }
    
    function mostrarVistaPrevia() {
        if (imagenInput.files && imagenInput.files[0]) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                imagenPreview.src = e.target.result;
                imagenPreviewContainer.style.display = 'block';
                imagenUploadArea.querySelector('.text-center').style.display = 'none';
            };
            
            reader.readAsDataURL(imagenInput.files[0]);
        }
    }
    
    // Eliminar imagen seleccionada
    if (eliminarImagen) {
        eliminarImagen.addEventListener('click', function() {
            imagenInput.value = '';
            imagenPreviewContainer.style.display = 'none';
            imagenUploadArea.querySelector('.text-center').style.display = 'block';
        });
    }
    
    // Validación y envío AJAX del formulario de registro de producto
    const registroProductoForm = document.getElementById('registroProductoForm');
    const alertMessage = document.getElementById('alert-message-productos');
    if (registroProductoForm) {
        registroProductoForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Validaciones
            const precio = document.getElementById('precio').value;
            if (parseFloat(precio) <= 0) {
                if (alertMessage) {
                    alertMessage.style.display = 'block';
                    alertMessage.style.backgroundColor = 'rgba(239, 68, 68, 0.1)';
                    alertMessage.style.color = 'var(--danger-color)';
                    alertMessage.style.border = '1px solid var(--danger-color)';
                    alertMessage.textContent = 'El precio debe ser mayor que cero.';
                }
                return false;
            }
            const existencia = document.getElementById('existencia').value;
            if (parseInt(existencia) < 0 || !Number.isInteger(parseFloat(existencia))) {
                if (alertMessage) {
                    alertMessage.style.display = 'block';
                    alertMessage.style.backgroundColor = 'rgba(239, 68, 68, 0.1)';
                    alertMessage.style.color = 'var(--danger-color)';
                    alertMessage.style.border = '1px solid var(--danger-color)';
                    alertMessage.textContent = 'La existencia debe ser un número entero positivo.';
                }
                return false;
            }
            // Usar FormData para enviar archivos
            const formData = new FormData(registroProductoForm);
            // Fecha actual si no se seleccionó
            if (!formData.get('fecha_ingreso')) {
                formData.set('fecha_ingreso', new Date().toISOString().slice(0, 10));
            }
            fetch(registroProductoForm.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.InformacionValida) {
                    if (alertMessage) {
                        alertMessage.style.display = 'block';
                        alertMessage.style.backgroundColor = 'rgba(16, 185, 129, 0.1)';
                        alertMessage.style.color = 'var(--success-color)';
                        alertMessage.style.border = '1px solid var(--success-color)';
                        alertMessage.textContent = data.message || 'Producto registrado exitosamente.';
                    }
                    registroProductoForm.reset();
                    // Actualizar lista de productos si existe la función global (como en manejoModal.js)
                    if (typeof window.actualizarListaProductos === 'function') {
                        window.actualizarListaProductos();
                    } else {
                        // Fallback: intentar actualizar la tabla manualmente
                        fetch('/api/productos/', {
                            method: 'GET',
                            headers: { 'X-Requested-With': 'XMLHttpRequest' }
                        })
                        .then(resp => resp.json())
                        .then(data => {
                            if (data.productos) {
                                const listaProductos = document.getElementById('lista-productos');
                                if (listaProductos) {
                                    listaProductos.innerHTML = '';
                                    data.productos.forEach(producto => {
                                        const productoRow = document.createElement('tr');
                                        productoRow.innerHTML = `
                                            <td><div class="producto-imagen">${producto.imagen ? `<img src="${producto.imagen}" alt="${producto.nombre_producto}" class="img-thumbnail">` : `<img src="/static/img/placeholder.jpg" alt="Sin imagen" class="img-thumbnail">`}</div></td>
                                            <td><div class="d-flex align-items-center"><div class="ms-3"><p class="fw-bold mb-1">${producto.nombre_producto}</p></div></div></td>
                                            <td>$${producto.precio}</td>
                                            <td><p class="descripcion-producto">${producto.descripcion}</p></td>
                                            <td>${producto.existencia} unidades</td>
                                            <td>${producto.tipo}</td>
                                            <td>${producto.estado === 'agotado' ? '<span class="badge badge-trashed rounded-pill d-inline">Agotado</span>' : '<span class="badge badge-success rounded-pill d-inline">Disponible</span>'}</td>
                                            <td><button class="btn btn-link btn-rounded btn-sm fw-bold editar-producto-btn" data-id="${producto.id_producto}"><i class="fas fa-edit"></i> Editar</button></td>
                                        `;
                                        listaProductos.appendChild(productoRow);
                                    });
                                }
                            }
                        });
                    }
                } else {
                    if (alertMessage) {
                        alertMessage.style.display = 'block';
                        alertMessage.style.backgroundColor = 'rgba(239, 68, 68, 0.1)';
                        alertMessage.style.color = 'var(--danger-color)';
                        alertMessage.style.border = '1px solid var(--danger-color)';
                        alertMessage.textContent = data.message || 'Error al registrar producto';
                    }
                }
            })
            .catch(error => {
                if (alertMessage) {
                    alertMessage.style.display = 'block';
                    alertMessage.style.backgroundColor = 'rgba(239, 68, 68, 0.1)';
                    alertMessage.style.color = 'var(--danger-color)';
                    alertMessage.style.border = '1px solid var(--danger-color)';
                    alertMessage.textContent = 'Error en el registro: ' + error;
                }
            });
        });
    }
});
