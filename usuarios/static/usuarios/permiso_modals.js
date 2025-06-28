// Lógica para abrir modales de permiso y cargar datos dinámicamente
function openPermisoModal(titulo, fieldsHtml, actionUrl) {
  document.getElementById('modalPermisoTitulo').innerText = titulo;
  document.getElementById('permisoFormFields').innerHTML = fieldsHtml;
  document.getElementById('permisoForm').action = actionUrl;
  openModal('modalPermiso');
}
function openPermisoDeleteModal(text, actionUrl) {
  document.getElementById('permisoDeleteText').innerHTML = text;
  document.getElementById('permisoDeleteForm').action = actionUrl;
  openModal('modalPermisoEliminar');
}
