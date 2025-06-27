document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const usernameError = document.getElementById('username-error');
    const passwordError = document.getElementById('password-error');
    const attemptsMessage = document.getElementById('attempts-message');
    const nIntentosInput = document.getElementById('n_intentos');
    const MAX_ATTEMPTS = 3;

    // Obtener intentos almacenados en localStorage o inicializar a 0
    let loginAttempts = parseInt(localStorage.getItem('loginAttempts') || '0');
    // Obtener n_intentos del backend si está disponible
    let backendAttempts = parseInt(document.body.getAttribute('data-n-intentos') || '0');
    // Usar el mayor valor entre localStorage y backend
    loginAttempts = Math.max(loginAttempts, backendAttempts);
    localStorage.setItem('loginAttempts', loginAttempts.toString());
    // Actualizar el input oculto con el valor actual de loginAttempts
    if (nIntentosInput) nIntentosInput.value = loginAttempts;

    // DEBUG: Mostrar los valores de loginAttempts y backendAttempts en consola
    console.log('DEBUG loginAttempts (localStorage):', localStorage.getItem('loginAttempts'));
    console.log('DEBUG backendAttempts (data-n-intentos):', backendAttempts);
    console.log('DEBUG loginAttempts (usado):', loginAttempts);

    // Si ya se excedió el número máximo de intentos, deshabilitar el formulario
    if (loginAttempts >= MAX_ATTEMPTS) {
        disableForm();
    }

    loginForm.addEventListener('submit', function(event) {
        resetErrors();
        let hasErrors = false;
        // Validar campos vacíos
        if (!usernameInput.value.trim()) {
            showError(usernameInput, usernameError, 'Por favor, ingresa tu nombre de usuario');
            hasErrors = true;
        }
        if (!passwordInput.value.trim()) {
            showError(passwordInput, passwordError, 'Por favor, ingresa tu contraseña');
            hasErrors = true;
        }
        if (hasErrors) {
            event.preventDefault();
            return;
        }
        // Antes de enviar, actualizar el input oculto con el valor actual de loginAttempts
        if (nIntentosInput) nIntentosInput.value = loginAttempts;
        // Si los campos están llenos, se permite el envío y la validación real la hace el backend
    });

    // Si hay mensaje de error del backend, contar intento fallido y mostrar intentos personalizados
    const backendError = document.querySelector('.message.error');
    if (backendError) {
        localStorage.setItem('loginAttempts', loginAttempts.toString());
        const errorText = '' + backendError.textContent;
        const remaining = MAX_ATTEMPTS - loginAttempts;
        let intentosMsg = ` Te quedan ${remaining} intento${remaining === 1 ? '' : 's'}.`;
        if (loginAttempts >= MAX_ATTEMPTS) {
            disableForm();
        } else if (errorText.includes('Usuario o contraseña incorrecta')) {
            // Usuario no existe: solo usuario en rojo y mensaje personalizado
            showError(usernameInput, usernameError, 'Usuario o contraseña incorrecta');
            showError(passwordInput, passwordError, 'Usuario o contraseña incorrecta');
            backendError.textContent = 'Usuario o contraseña incorrecta.' + intentosMsg;
        } else if (errorText.includes('contraseña incorrecta')) {
            // Contraseña incorrecta: solo contraseña en rojo y mensaje personalizado
            showError(passwordInput, passwordError, 'Usuario o contraseña incorrecta');
            showError(usernameInput, usernameError, 'Usuario o contraseña incorrecta');
            backendError.textContent = 'Usuario o contraseña incorrecta.' + intentosMsg;
        }
    }

    // Mostrar errores visuales al enfocar
    usernameInput.addEventListener('focus', function() {
        this.classList.remove('error');
        usernameError.textContent = '';
    });
    passwordInput.addEventListener('focus', function() {
        this.classList.remove('error');
        passwordError.textContent = '';
    });

    function showError(input, errorElement, message) {
        input.classList.add('error');
        errorElement.textContent = message;
    }
    function resetErrors() {
        usernameInput.classList.remove('error');
        passwordInput.classList.remove('error');
        usernameError.textContent = '';
        passwordError.textContent = '';
    }
    function disableForm() {
        usernameInput.disabled = true;
        passwordInput.disabled = true;
        document.querySelector('.btn-login').disabled = true;
        attemptsMessage.classList.remove('hidden');
    }

    // Oculta los mensajes después de 3 segundos
    setTimeout(function() {
        var msg = document.getElementById('messages-container');
        if(msg) { msg.style.display = 'none'; }
    }, 2000);
});
