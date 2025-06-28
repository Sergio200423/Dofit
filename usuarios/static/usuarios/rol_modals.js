// Lógica para abrir modales de rol y cargar datos dinámicamente
function openRolModal(titulo, fieldsHtml, actionUrl) {
  document.getElementById('modalRolTitulo').innerText = titulo;
  document.getElementById('rolFormFields').innerHTML = fieldsHtml;
  document.getElementById('rolForm').action = actionUrl;
  openModal('modalRol');
}
function openRolDeleteModal(text, actionUrl) {
  document.getElementById('rolDeleteText').innerHTML = text;
  document.getElementById('rolDeleteForm').action = actionUrl;
  openModal('modalRolEliminar');
}
