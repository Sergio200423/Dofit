document.addEventListener('DOMContentLoaded', function() {
    // Seleccionar elementos
    const btnEnviar = document.getElementById('btn-enviar');
    const userItems = document.querySelectorAll('.user-item');
    const form = document.getElementById('form-correos');

    function updateButtonState() {
        const checkboxes = document.querySelectorAll('input[type=checkbox][name=correo]');
        const isAnyChecked = Array.from(checkboxes).some(checkbox => checkbox.checked);
        if (isAnyChecked) {
            btnEnviar.disabled = false;
            btnEnviar.classList.add('active');
        } else {
            btnEnviar.disabled = true;
            btnEnviar.classList.remove('active');
        }
    }

    // Permitir solo un checkbox seleccionado a la vez (comportamiento tipo radio)
    form.addEventListener('input', function(e) {
        if (e.target && e.target.type === 'checkbox' && e.target.name === 'correo') {
            if (e.target.checked) {
                // Desmarcar todos los demás
                document.querySelectorAll('input[type=checkbox][name=correo]').forEach(cb => {
                    if (cb !== e.target) cb.checked = false;
                });
            }
            updateButtonState();
            // Animar el elemento padre cuando se selecciona
            userItems.forEach(item => {
                item.style.borderColor = '';
                item.style.boxShadow = '';
            });
            const userItem = e.target.closest('.user-item');
            if (e.target.checked) {
                userItem.style.borderColor = 'var(--primary-color)';
                userItem.style.boxShadow = '0 4px 12px rgba(26, 115, 232, 0.2)';
            }
        }
    });

    // Añadir efecto hover a los elementos de usuario
    userItems.forEach(item => {
        if (!item.classList.contains('disabled')) {
            item.addEventListener('mouseenter', function() {
                this.style.transform = 'translateX(5px)';
            });
            item.addEventListener('mouseleave', function() {
                this.style.transform = '';
            });
        }
    });

    // Animación para el botón de email
    const emailButton = document.querySelector('.email-button');
    if (emailButton) {
        emailButton.addEventListener('mouseenter', function() {
            if (!this.disabled) {
                const outerCircle = this.querySelector('.email-circle-outer');
                if (outerCircle) {
                    outerCircle.style.animationDuration = '4s';
                }
            }
        });
        emailButton.addEventListener('mouseleave', function() {
            const outerCircle = this.querySelector('.email-circle-outer');
            if (outerCircle) {
                outerCircle.style.animationDuration = '8s';
            }
        });
    }

    // Inicializar el estado del botón
    updateButtonState();

    // Animación de entrada para el formulario
    const card = document.querySelector('.card');
    setTimeout(() => {
        card.style.opacity = '1';
        card.style.transform = 'translateY(0)';
    }, 100);

    // Validación del formulario
    form.addEventListener('submit', function(event) {
        const checkboxes = document.querySelectorAll('input[type=checkbox][name=correo]');
        const isAnyChecked = Array.from(checkboxes).some(checkbox => checkbox.checked);
        if (!isAnyChecked) {
            event.preventDefault();
            alert('Por favor, seleccione un usuario para enviar el correo de cambio de contraseña.');
        }
    });

    // Quitar el atributo 'required' de los checkboxes para evitar el mensaje por defecto del navegador
    document.querySelectorAll('input[type=checkbox][name=correo]').forEach(cb => {
        cb.removeAttribute('required');
    });

    // Ocultar visualmente el checkbox pero dejarlo clickeable
    const style = document.createElement('style');
    style.innerHTML = `
    .user-checkbox input[type="checkbox"] {
        opacity: 0;
        width: 20px;
        height: 20px;
        margin: 0;
        position: absolute;
        left: 0;
        top: 0;
        z-index: 2;
        cursor: pointer;
    }
    .user-checkbox {
        position: relative;
        display: flex;
        align-items: center;
        min-height: 24px;
    }
    `;
    document.head.appendChild(style);
});