// Lógica para abrir modales de usuario y cargar datos dinámicamente
function openUsuarioModal(titulo, fieldsHtml, actionUrl) {
  document.getElementById('modalUsuarioTitulo').innerText = titulo;
  document.getElementById('usuarioFormFields').innerHTML = fieldsHtml;
  document.getElementById('usuarioForm').action = actionUrl;
  openModal('modalUsuario');
}
function openUsuarioDeleteModal(text, actionUrl) {
  document.getElementById('usuarioDeleteText').innerHTML = text;
  document.getElementById('usuarioDeleteForm').action = actionUrl;
  openModal('modalUsuarioEliminar');
}
