// Script para manejar el modal de edición de productos

document.addEventListener('DOMContentLoaded', function() {
    // Referencias a elementos del DOM para la edición de productos
    const editarProductoModal = document.getElementById('editarProductoModal');
    const editarProductoForm = document.getElementById('editarProductoForm');
    const cambiarImagenCheckbox = document.getElementById('cambiarImagen');
    const editarImagenContainer = document.getElementById('editarImagenContainer');
    const editarImagenInput = document.getElementById('editar_imagen');
    const editarImagenUploadArea = document.getElementById('editarImagenUploadArea');
    const editarImagenPreviewContainer = document.getElementById('editarImagenPreviewContainer');
    const editarImagenPreview = document.getElementById('editarImagenPreview');
    const editarEliminarImagen = document.getElementById('editarEliminarImagen');
    
    // Botones de editar en la tabla
    const editarBtns = document.querySelectorAll('.editar-producto-btn');
    
    // Manejar clics en los botones de editar
    editarBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const productoId = this.getAttribute('data-id');
            cargarDatosProducto(productoId);
        });
    });
    
    // Función para cargar los datos del producto en el modal
    function cargarDatosProducto(productoId) {
        // Actualizar el ID del producto en el formulario
        document.getElementById('editar_producto_id').value = productoId;
        
        // Actualizar la acción del formulario
        editarProductoForm.action = editarProductoForm.action.replace(/\/\d+\/$/, `/${productoId}/`);
        
        // Hacer una petición AJAX para obtener los datos del producto
        fetch(`/productos/obtener/${productoId}/`)
            .then(response => response.json())
            .then(data => {
                // Llenar el formulario con los datos del producto
                document.getElementById('editar_nombre_producto').value = data.nombre_producto;
                document.getElementById('editar_precio').value = data.precio;
                document.getElementById('editar_descripcion').value = data.descripcion;
                document.getElementById('editar_tipo').value = data.tipo;
                document.getElementById('editar_existencia').value = data.existencia;
                document.getElementById('editar_estado').value = data.estado;
                
                // Mostrar la imagen actual si existe
                const imagenActualContainer = document.getElementById('imagenActualContainer');
                const imagenActual = document.getElementById('imagenActual');
                
                if (data.imagen_url) {
                    imagenActual.src = data.imagen_url;
                    imagenActualContainer.style.display = 'block';
                } else {
                    imagenActualContainer.style.display = 'none';
                }
                
                // Mostrar el modal
                const modalInstance = new bootstrap.Modal(editarProductoModal);
                modalInstance.show();
            })
            .catch(error => {
                console.error('Error al cargar los datos del producto:', error);
                alert('Error al cargar los datos del producto. Por favor, intenta de nuevo.');
            });
    }
    
    // Manejar el checkbox para cambiar la imagen
    if (cambiarImagenCheckbox) {
        cambiarImagenCheckbox.addEventListener('change', function() {
            if (this.checked) {
                editarImagenContainer.style.display = 'block';
            } else {
                editarImagenContainer.style.display = 'none';
                editarImagenInput.value = '';
                editarImagenPreviewContainer.style.display = 'none';
                editarImagenUploadArea.querySelector('.text-center').style.display = 'block';
            }
        });
    }
    
    // Manejar la carga de imágenes en el formulario de edición
    if (editarImagenUploadArea) {
        editarImagenUploadArea.addEventListener('click', function() {
            editarImagenInput.click();
        });
        
        // Arrastrar y soltar imágenes
        editarImagenUploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            editarImagenUploadArea.classList.add('border-primary');
        });
        
        editarImagenUploadArea.addEventListener('dragleave', function() {
            editarImagenUploadArea.classList.remove('border-primary');
        });
        
        editarImagenUploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            editarImagenUploadArea.classList.remove('border-primary');
            
            if (e.dataTransfer.files.length) {
                editarImagenInput.files = e.dataTransfer.files;
                mostrarVistaPrevia();
            }
        });
    }
    
    // Mostrar vista previa de la imagen seleccionada en el formulario de edición
    if (editarImagenInput) {
        editarImagenInput.addEventListener('change', mostrarVistaPrevia);
    }
    
    function mostrarVistaPrevia() {
        if (editarImagenInput.files && editarImagenInput.files[0]) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                editarImagenPreview.src = e.target.result;
                editarImagenPreviewContainer.style.display = 'block';
                editarImagenUploadArea.querySelector('.text-center').style.display = 'none';
            };
            
            reader.readAsDataURL(editarImagenInput.files[0]);
        }
    }
    
    // Eliminar imagen seleccionada en el formulario de edición
    if (editarEliminarImagen) {
        editarEliminarImagen.addEventListener('click', function() {
            editarImagenInput.value = '';
            editarImagenPreviewContainer.style.display = 'none';
            editarImagenUploadArea.querySelector('.text-center').style.display = 'block';
        });
    }
    
    // Validación del formulario de edición antes de enviar
    if (editarProductoForm) {
        editarProductoForm.addEventListener('submit', function(e) {
            // Aquí puedes agregar validaciones adicionales si es necesario
            
            // Por ejemplo, validar que el precio sea mayor que cero
            const precio = document.getElementById('editar_precio').value;
            if (parseFloat(precio) <= 0) {
                e.preventDefault();
                alert('El precio debe ser mayor que cero.');
                return false;
            }
            
            // Validar que la existencia sea un número entero positivo
            const existencia = document.getElementById('editar_existencia').value;
            if (parseInt(existencia) < 0 || !Number.isInteger(parseFloat(existencia))) {
                e.preventDefault();
                alert('La existencia debe ser un número entero positivo.');
                return false;
            }
            
            // Si todo está bien, el formulario se enviará normalmente
        });
    }
});
