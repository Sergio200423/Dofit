document.addEventListener("DOMContentLoaded", () => {
  const inputs = document.querySelectorAll(".code-input")

  let contadorElemento = document.getElementById("contador")
  let contadorSegundosElemento = document.getElementById("segundos")
  const TemporizadorInicio = Date.now();

  const alerta = document.getElementById("alert-message");


  // Enfocar el primer input al cargar la página
  if (inputs.length > 0) {
    setTimeout(() => {
      inputs[0].focus()
    }, 100)
  }

  // Manejar la navegación entre inputs
  inputs.forEach((input, index) => {
    // Avanzar al siguiente input cuando se ingresa un dígito
    input.addEventListener("input", (e) => {
      // Asegurar que solo se ingresen números
      e.target.value = e.target.value.replace(/\D/g, "")

      if (e.target.value && index < inputs.length - 1) {
        inputs[index + 1].focus()
      }
    })

    // Retroceder al input anterior con la tecla Backspace
    input.addEventListener("keydown", (e) => {
      if (e.key === "Backspace" && !e.target.value && index > 0) {
        inputs[index - 1].focus()
      }
    })
  })

  // Permitir pegar el código completo
  inputs.forEach((input) => {
    input.addEventListener("paste", (e) => {
      e.preventDefault()
      const paste = (e.clipboardData || window.clipboardData).getData("text")

      // Si el texto pegado contiene 4 dígitos
      if (/^\d{4}$/.test(paste)) {
        for (let i = 0; i < inputs.length; i++) {
          inputs[i].value = paste[i] || ""
        }
        // Enfocar el último input después de pegar
        inputs[inputs.length - 1].focus()
      }
    })
  })

  // Enviar el formulario cuando se completen todos los campos
  inputs[inputs.length - 1].addEventListener("input", () => {
    const allFilled = Array.from(inputs).every((input) => input.value.length === 1)
    if (allFilled) {
      // Opcional: enviar el formulario automáticamente
      clearInterval(TemporizadorID); // Detener temporizador si se envía
      document.querySelector('form').submit();
    }
  })

  // Iniciar temporizador que deshabilita los inputs tras 60 segundos
  const TemporizadorID = setInterval(calcularTiempoRestante, 1000);
  let contadorIntervalo = setInterval(() => {
    const tiempoRestante = 60 - Math.floor((Date.now() - TemporizadorInicio) / 1000);
    if (tiempoRestante >= 1) {
      contadorElemento.textContent = tiempoRestante;
    }
    else{
      if (contadorElemento) {
        contadorElemento.classList.remove('contador');
        contadorElemento.hidden = true; // Ocultar el contador
      }
      if (contadorSegundosElemento) {
        contadorSegundosElemento.hidden = true; // Ocultar el texto "segundos"
        contadorSegundosElemento.classList.remove('contador-segundos');
      }
    }// Cambiar color del contador
  }, 1000);

  function calcularTiempoRestante(){
    const tiempoTranscurridoSegundos = Math.floor((Date.now() - TemporizadorInicio) / 1000);
    if(tiempoTranscurridoSegundos >= 60)
    {
      inputs.forEach((input) => {
        input.disabled = true;
      });
      alerta.style.display = "block"; // Mostrar alerta
      alerta.style.color = 'red'; // Cambiar color de la alerta
      alerta.textContent = "El tiempo ha expirado. Por favor, vuelve a solicitar el código.";
      clearInterval(TemporizadorID); // Detener temporizador al deshabilitar
    }
  }
})