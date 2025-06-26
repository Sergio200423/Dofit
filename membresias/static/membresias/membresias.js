// Script para la página de membresías
document.addEventListener('DOMContentLoaded', function() {
    // Seleccionar todos los botones de "Añadir al carrito"
    const botonesCarrito = document.querySelectorAll('.btn-carrito');
    
    // Contador de items en el carrito (puedes integrarlo con tu sistema existente)
    let itemsEnCarrito = 0;
    
    // Añadir event listeners a cada botón
    botonesCarrito.forEach(boton => {
        boton.addEventListener('click', function() {
            const membresia = this.getAttribute('data-id');
            const precio = this.getAttribute('data-precio');
            
            // Añadir al carrito
            agregarAlCarrito(membresia, precio);
            
            // Cambiar el texto del botón temporalmente
            const textoOriginal = this.textContent;
            this.textContent = '¡Añadido!';
            this.style.backgroundColor = '#00cc66';
            this.style.borderColor = '#00cc66';
            this.style.color = 'white';
            
            // Restaurar el texto original después de 2 segundos
            setTimeout(() => {
                this.textContent = textoOriginal;
                this.style.backgroundColor = '';
                this.style.borderColor = '';
                this.style.color = '';
            }, 2000);
        });
    });
    
    // Función para añadir al carrito
    function agregarAlCarrito(membresia, precio) {
        // Aquí puedes implementar la lógica para añadir al carrito
        // Por ejemplo, enviar una petición AJAX a tu backend de Django
        console.log(`Membresía añadida: ${membresia}, Precio: C$${precio}`);
        
        // Incrementar contador
        itemsEnCarrito++;
        
        // Puedes mostrar una notificación o actualizar un contador en la UI
        mostrarNotificacion(`Membresía ${membresia} añadida al carrito`);
        
        // Si tienes un contador de carrito en tu UI, puedes actualizarlo aquí
        // actualizarContadorCarrito(itemsEnCarrito);
    }

    // Seleccionar todos los botones de "Editar"
    const botonesEditar = document.querySelectorAll('.btn-editar');
    
    // Seleccionar elementos del modal
    const modal = document.getElementById('modal-editar');
    const modalClose = document.querySelector('.modal-close');
    const btnCancelar = document.querySelector('.btn-cancelar');
    const tipoMembresia = document.getElementById('tipo-membresia');
    const formEditarMembresia = document.getElementById('form-editar-membresia');
    const inputMembresia = document.getElementById('membresia_id');
    const inputTipoMembresia = document.getElementById('tipo_membresia');
    
    // Añadir event listeners a cada botón de editar
    botonesEditar.forEach(boton => {
        boton.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            const tipo = this.getAttribute('data-tipo');
            const precio = this.getAttribute('data-precio');
            
            // Establecer valores en el formulario
            inputMembresia.value = id;
            inputTipoMembresia.value = tipo;
            tipoMembresia.textContent = tipo;
            
            // Establecer fechas por defecto
            const hoy = new Date();
            const fechaInicio = formatDate(hoy);
            
            // Calcular fecha fin según el tipo de membresía
            let fechaFin;
            if (id === 'trimestral') {
                // 3 meses
                const tresM = new Date(hoy);
                tresM.setMonth(hoy.getMonth() + 3);
                fechaFin = formatDate(tresM);
            } else if (id === 'anual') {
                // 12 meses
                const unA = new Date(hoy);
                unA.setFullYear(hoy.getFullYear() + 1);
                fechaFin = formatDate(unA);
            } else {
                // 1 mes por defecto
                const unM = new Date(hoy);
                unM.setMonth(hoy.getMonth() + 1);
                fechaFin = formatDate(unM);
            }
            
            document.getElementById('fecha_inicio').value = fechaInicio;
            document.getElementById('fecha_fin').value = fechaFin;
            
            // Mostrar el modal
            abrirModal();
        });
    });
    
    // Función para formatear fecha a YYYY-MM-DD
    function formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }
    
    // Función para abrir el modal
    function abrirModal() {
        modal.classList.add('show');
    }
    
    // Función para cerrar el modal
    function cerrarModal() {
        modal.classList.remove('show');
        setTimeout(() => {
            modal.style.display = 'none';
        }, 300);
    }
    
    // Event listeners para cerrar el modal
    modalClose.addEventListener('click', cerrarModal);
    btnCancelar.addEventListener('click', cerrarModal);
    
    // Cerrar el modal al hacer clic fuera del contenido
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            cerrarModal();
        }
    });
    
    // Manejar el envío del formulario
    formEditarMembresia.addEventListener('submit', function(event) {
        // Si quieres manejar el envío con AJAX, descomenta la siguiente línea
        // event.preventDefault();
        
        // Aquí puedes añadir validación adicional si es necesario
        const fechaInicio = new Date(document.getElementById('fecha_inicio').value);
        const fechaFin = new Date(document.getElementById('fecha_fin').value);
        
        if (fechaFin <= fechaInicio) {
            event.preventDefault();
            alert('La fecha de fin debe ser posterior a la fecha de inicio');
            return false;
        }
        
        // Si todo está bien, el formulario se enviará normalmente
        // O puedes manejarlo con AJAX si prefieres
        
        // Ejemplo de envío con AJAX (descomenta si quieres usar AJAX)
        /*
        event.preventDefault();
        
        const formData = new FormData(this);
        
        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                mostrarNotificacion('Membresía actualizada correctamente');
                cerrarModal();
                // Opcionalmente, recargar la página o actualizar la UI
                // window.location.reload();
            } else {
                mostrarNotificacion('Error: ' + data.error, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            mostrarNotificacion('Error al procesar la solicitud', 'error');
        });
        */
    });
    
    // Función para mostrar notificación
    function mostrarNotificacion(mensaje, tipo = 'success') {
        // Crear elemento de notificación
        const notificacion = document.createElement('div');
        notificacion.className = 'notificacion ' + tipo;
        notificacion.textContent = mensaje;
        
        // Estilos para la notificación
        notificacion.style.position = 'fixed';
        notificacion.style.bottom = '20px';
        notificacion.style.right = '20px';
        notificacion.style.backgroundColor = tipo === 'success' ? '#0066ff' : '#ff3333';
        notificacion.style.color = 'white';
        notificacion.style.padding = '10px 20px';
        notificacion.style.borderRadius = '4px';
        notificacion.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.2)';
        notificacion.style.zIndex = '1000';
        notificacion.style.opacity = '0';
        notificacion.style.transform = 'translateY(20px)';
        notificacion.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        
        // Añadir al DOM
        document.body.appendChild(notificacion);
        
        // Mostrar con animación
        setTimeout(() => {
            notificacion.style.opacity = '1';
            notificacion.style.transform = 'translateY(0)';
        }, 10);
        
        // Ocultar después de 3 segundos
        setTimeout(() => {
            notificacion.style.opacity = '0';
            notificacion.style.transform = 'translateY(20px)';
            
            // Eliminar del DOM después de la animación
            setTimeout(() => {
                document.body.removeChild(notificacion);
            }, 300);
        }, 3000);
    }
    
    // Función para efectos visuales en las tarjetas
    function inicializarEfectosTarjetas() {
        const tarjetas = document.querySelectorAll('.membresia-card');
        
        tarjetas.forEach(tarjeta => {
            // Añadir efecto de elevación al pasar el mouse
            tarjeta.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-5px)';
                this.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.2)';
            });
            
            tarjeta.addEventListener('mouseleave', function() {
                this.style.transform = '';
                this.style.boxShadow = '';
            });
        });
    }
    
    // Inicializar efectos visuales
    inicializarEfectosTarjetas();
});