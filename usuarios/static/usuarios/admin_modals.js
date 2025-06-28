// Lógica para abrir modales de administrador y cargar datos dinámicamente
function openAdminModal(titulo, fieldsHtml, actionUrl) {
  document.getElementById('modalAdminTitulo').innerText = titulo;
  document.getElementById('adminFormFields').innerHTML = fieldsHtml;
  document.getElementById('adminForm').action = actionUrl;
  openModal('modalAdmin');
}
function openAdminDeleteModal(text, actionUrl) {
  document.getElementById('adminDeleteText').innerHTML = text;
  document.getElementById('adminDeleteForm').action = actionUrl;
  openModal('modalAdminEliminar');
}
