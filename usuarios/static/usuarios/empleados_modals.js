// Lógica para abrir modales de empleado y cargar datos dinámicamente
function openEmpleadoModal(titulo, fieldsHtml, actionUrl) {
  document.getElementById('modalEmpleadoTitulo').innerText = titulo;
  document.getElementById('empleadoFormFields').innerHTML = fieldsHtml;
  document.getElementById('empleadoForm').action = actionUrl;
  openModal('modalEmpleado');
}
function openEmpleadoDeleteModal(text, actionUrl) {
  document.getElementById('empleadoDeleteText').innerHTML = text;
  document.getElementById('empleadoDeleteForm').action = actionUrl;
  openModal('modalEmpleadoEliminar');
}
