document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const modal = document.getElementById('modalRol');
    const btnAgregarRol = document.getElementById('btnAgregarRol');
    const btnCancelar = document.getElementById('btnCancelar');
    const closeBtn = document.querySelector('.close');
    const formRol = document.getElementById('formRol');
    const modalTitle = document.getElementById('modalTitle');
    const rolIdInput = document.getElementById('rolId');
    const nombreInput = document.getElementById('nombre');
    const descripcionInput = document.getElementById('descripcion');
    
    // Botones de editar y eliminar
    const btnEdit = document.querySelectorAll('.btn-edit');
    const btnDelete = document.querySelectorAll('.btn-delete');

    // Función para abrir el modal
    function abrirModal(titulo = 'Agregar Rol', esEdicion = false) {
        modalTitle.textContent = titulo;
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden'; // Prevenir scroll del body
        
        // Focus en el primer input
        setTimeout(() => {
            nombreInput.focus();
        }, 100);
    }

    // Función para cerrar el modal
    function cerrarModal() {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto'; // Restaurar scroll del body
        limpiarFormulario();
        limpiarErrores();
    }

    // Función para limpiar el formulario
    function limpiarFormulario() {
        formRol.reset();
        rolIdInput.value = '';
        // Cambiar la acción del formulario para crear
        formRol.action = formRol.action.replace(/\/editar\/\d+\/$/, '/crear/');
    }

    // Función para limpiar mensajes de error
    function limpiarErrores() {
        const errorMessages = document.querySelectorAll('.error-message');
        errorMessages.forEach(error => {
            error.style.display = 'none';
            error.textContent = '';
        });
        
        // Remover clases de error de los inputs
        const inputs = document.querySelectorAll('.form-group input, .form-group textarea');
        inputs.forEach(input => {
            input.style.borderColor = '#ecf0f1';
        });
    }

    // Función para mostrar errores
    function mostrarError(campo, mensaje) {
        const errorElement = document.getElementById(error${campo.charAt(0).toUpperCase() + campo.slice(1)});
        const inputElement = document.getElementById(campo);
        
        if (errorElement && inputElement) {
            errorElement.textContent = mensaje;
            errorElement.style.display = 'block';
            inputElement.style.borderColor = '#e74c3c';
        }
    }

    // Función para validar el formulario
    function validarFormulario() {
        let esValido = true;
        limpiarErrores();

        // Validar nombre
        const nombre = nombreInput.value.trim();
        if (!nombre) {
            mostrarError('nombre', 'El nombre del rol es obligatorio');
            esValido = false;
        } else if (nombre.length > 50) {
            mostrarError('nombre', 'El nombre no puede exceder 50 caracteres');
            esValido = false;
        }

        // Validar descripción (opcional, pero si se proporciona, validar longitud)
        const descripcion = descripcionInput.value.trim();
        if (descripcion.length > 500) {
            mostrarError('descripcion', 'La descripción no puede exceder 500 caracteres');
            esValido = false;
        }

        return esValido;
    }

    // Event Listeners

    // Abrir modal para agregar rol
    btnAgregarRol.addEventListener('click', function() {
        abrirModal('Agregar Rol', false);
    });

    // Cerrar modal
    btnCancelar.addEventListener('click', cerrarModal);
    closeBtn.addEventListener('click', cerrarModal);

    // Cerrar modal al hacer clic fuera de él
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            cerrarModal();
        }
    });

    // Cerrar modal con la tecla Escape
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && modal.style.display === 'block') {
            cerrarModal();
        }
    });

    // Manejar envío del formulario
    formRol.addEventListener('submit', function(event) {
        event.preventDefault();
        
        if (!validarFormulario()) {
            return;
        }

        // Aquí puedes agregar lógica adicional antes del envío
        // Por ejemplo, mostrar un loader
        const btnGuardar = document.getElementById('btnGuardar');
        const textoOriginal = btnGuardar.textContent;
        btnGuardar.textContent = 'Guardando...';
        btnGuardar.disabled = true;

        // Simular envío (en producción, esto sería una petición AJAX)
        setTimeout(() => {
            // Restaurar botón
            btnGuardar.textContent = textoOriginal;
            btnGuardar.disabled = false;
            
            // En un caso real, aquí manejarías la respuesta del servidor
            // Por ahora, simplemente enviamos el formulario
            formRol.submit();
        }, 1000);
    });

    // Manejar botones de editar
    btnEdit.forEach(button => {
        button.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            const nombre = this.getAttribute('data-nombre');
            const descripcion = this.getAttribute('data-descripcion');
            
            // Llenar el formulario con los datos existentes
            rolIdInput.value = id;
            nombreInput.value = nombre;
            descripcionInput.value = descripcion || '';
            
            // Cambiar la acción del formulario para editar
            formRol.action = formRol.action.replace('/crear/', /editar/${id}/);
            
            abrirModal('Editar Rol', true);
        });
    });

    // Manejar botones de eliminar
    btnDelete.forEach(button => {
        button.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            const nombre = this.closest('tr').querySelector('td:nth-child(2)').textContent;
            
            if (confirm(¿Estás seguro de que deseas eliminar el rol "${nombre}"?)) {
                // Crear formulario para eliminar
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = /roles/eliminar/${id}/;
                
                // Agregar token CSRF
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                const csrfInput = document.createElement('input');
                csrfInput.type = 'hidden';
                csrfInput.name = 'csrfmiddlewaretoken';
                csrfInput.value = csrfToken;
                form.appendChild(csrfInput);
                
                document.body.appendChild(form);
                form.submit();
            }
        });
    });

    // Validación en tiempo real
    nombreInput.addEventListener('input', function() {
        if (this.value.trim()) {
            this.style.borderColor = '#27ae60';
            document.getElementById('errorNombre').style.display = 'none';
        }
    });

    descripcionInput.addEventListener('input', function() {
        const maxLength = 500;
        const currentLength = this.value.length;
        
        if (currentLength > maxLength) {
            this.style.borderColor = '#e74c3c';
            mostrarError('descripcion', La descripción excede el límite (${currentLength}/${maxLength}));
        } else {
            this.style.borderColor = '#ecf0f1';
            document.getElementById('errorDescripcion').style.display = 'none';
        }
    });
});