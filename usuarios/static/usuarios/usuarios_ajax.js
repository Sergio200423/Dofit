// AJAX para cargar y enviar formularios de usuario en modales
function cargarFormularioUsuario(url, titulo) {
  fetch(url)
    .then(response => response.text())
    .then(html => {
      document.getElementById('modalUsuarioTitulo').innerText = titulo;
      document.getElementById('usuarioFormFields').innerHTML = html;
      openModal('modalUsuario');
      asociarSubmitUsuarioForm(); // <-- Asegura el submit AJAX tras cada carga
    });
}

function asociarSubmitUsuarioForm() {
  const form = document.getElementById('usuarioForm');
  if (form) {
    form.onsubmit = function(e) {
      e.preventDefault();
      const url = form.action;
      const formData = new FormData(form);
      fetch(url, {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          location.reload();
        } else {
          document.getElementById('usuarioFormFields').innerHTML = data.form_html;
          asociarSubmitUsuarioForm(); // <-- Reasocia el submit tras error
        }
      });
    };
  }
}

document.addEventListener('DOMContentLoaded', function() {
  asociarSubmitUsuarioForm(); // Inicial
});
