document.addEventListener('DOMContentLoaded', function() {
    // Variables globales y referencias DOM
    const form = document.getElementById('verificationForm');
    const inputs = document.querySelectorAll('.code-input');
    const timerValue = document.getElementById('timerValue');
    const attemptsValue = document.getElementById('attemptsValue');
    const timerContainer = document.getElementById('timerContainer');
    const expiredMessage = document.getElementById('expiredMessage');
    const submitBtn = document.getElementById('submitBtn');

    // Tomar los intentos desde el backend, si no existe, poner 0
    let attemptsLeft = (form && form.hasAttribute('data-intentos')) ? parseInt(form.getAttribute('data-intentos')) || 0 : 0;
    let timeLeft = 180; // 3 minutos en segundos
    let timerInterval;
    let isExpired = false;

    // Función para formatear el tiempo
    function formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
    }

    // Función para actualizar el timer
    function updateTimer() {
        timerValue.textContent = formatTime(timeLeft);
        if (timeLeft <= 30) {
            timerValue.className = 'timer-value danger';
        } else if (timeLeft <= 60) {
            timerValue.className = 'timer-value warning';
        } else {
            timerValue.className = 'timer-value';
        }
        if (timeLeft <= 0) {
            expireSession();
        }
        timeLeft--;
    }

    // Función para actualizar los intentos
    function updateAttempts() {
        attemptsValue.textContent = attemptsLeft;
        if (attemptsLeft <= 1) {
            attemptsValue.className = 'attempts-value danger';
        } else if (attemptsLeft <= 2) {
            attemptsValue.className = 'attempts-value warning';
        } else {
            attemptsValue.className = 'attempts-value';
        }
    }

    // Función para expirar la sesión
    function expireSession() {
        isExpired = true;
        clearInterval(timerInterval);
        inputs.forEach(input => {
            input.disabled = true;
            input.value = '';
        });
        submitBtn.disabled = true;
        timerContainer.style.display = 'none';
        expiredMessage.style.display = 'block';
        expiredMessage.classList.remove('visually-hidden');
    }

    // Función para manejar intento fallido
    function handleFailedAttempt() {
        if (isExpired) return;
        attemptsLeft--;
        updateAttempts();
        inputs.forEach(input => {
            input.value = '';
        });
        if (attemptsLeft <= 0) {
            expireSession();
        } else {
            inputs[0].focus();
        }
    }

    // Iniciar el timer
    function startTimer() {
        updateTimer();
        timerInterval = setInterval(updateTimer, 1000);
    }

    // Lógica original de los inputs
    inputs.forEach((input, index) => {
        input.addEventListener('input', (e) => {
            if (isExpired) return;
            if (e.target.value && index < inputs.length - 1) {
                inputs[index + 1].focus();
            } else if (e.target.value && index === inputs.length - 1) {
                input.blur();
            }
        });
        input.addEventListener('keydown', (e) => {
            if (isExpired) return;
            if (e.key === 'Backspace' && index > 0 && !e.target.value) {
                inputs[index - 1].focus();
            }
        });
    });

    // Permitir pegar el código completo en cualquier input
    inputs.forEach((input, index) => {
        input.addEventListener('paste', (e) => {
            if (isExpired) return;
            const paste = (e.clipboardData || window.clipboardData).getData('text');
            if (/^\d{4}$/.test(paste)) {
                for (let i = 0; i < 4; i++) {
                    if (inputs[i]) inputs[i].value = paste[i] || '';
                }
                inputs.forEach(inp => inp.blur());
                e.preventDefault();
            }
        });
    });

    // Validar que solo se puedan ingresar números en los inputs
    inputs.forEach((input) => {
        input.addEventListener('input', (e) => {
            if (isExpired) return;
            e.target.value = e.target.value.replace(/\D/g, '');
        });
        input.addEventListener('keypress', (e) => {
            if (isExpired) return;
            if (!/\d/.test(e.key)) {
                e.preventDefault();
            }
        });
    });

    // Manejar envío del formulario
    if (form) {
        form.addEventListener('submit', function(e) {
            if (isExpired) {
                e.preventDefault();
                return;
            }
            // Siempre permitir el submit para que el backend maneje la validación y los intentos
            // (El siguiente bloque queda comentado para depuración)
            /*
            const codigoGenerado = form.getAttribute('data-codigo');
            let codigoIngresado = '';
            inputs.forEach(input => {
                codigoIngresado += input.value;
            });
            if (codigoIngresado.length === 4 && codigoGenerado && codigoIngresado !== codigoGenerado) {
                e.preventDefault();
                handleFailedAttempt();
                Swal.fire({
                    icon: 'error',
                    title: 'Código incorrecto',
                    text: 'El código ingresado no es válido. Intenta de nuevo.',
                    confirmButtonColor: '#2575fc'
                });
                return;
            }
            */
            // Si es correcto, el backend validará igual, pero permitimos el submit
        });
    }

    // Actualizar intentos desde backend si el formulario se recarga
    if (form && form.hasAttribute('data-intentos')) {
        attemptsLeft = parseInt(form.getAttribute('data-intentos')) || 0;
        updateAttempts();
        if (attemptsLeft <= 0) {
            expireSession();
        }
    }
    const firstInput = document.querySelector('.code-input');
    if (firstInput) {
        firstInput.focus();
    }
    // Solo iniciar el timer si no está expirado
    if (attemptsLeft > 0 && !isExpired) {
        startTimer();
    }
    updateAttempts();

    // Si el backend activa el mensaje de expiración, bloquear todo igual que en frontend
    const expiredDiv = document.getElementById('expiredMessage');
    if (expiredDiv && !expiredDiv.classList.contains('visually-hidden')) {
        inputs.forEach(input => {
            input.disabled = true;
            input.value = '';
        });
        submitBtn.disabled = true;
        timerContainer.style.display = 'none';
    }
});
