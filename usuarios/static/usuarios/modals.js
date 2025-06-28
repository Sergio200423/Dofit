// Lógica básica para abrir/cerrar modales y cargar datos en formularios
function openModal(modalId) {
  document.getElementById(modalId).style.display = 'block';
}
function closeModal(modalId) {
  document.getElementById(modalId).style.display = 'none';
}
// Cerrar modal al hacer click fuera
window.onclick = function(event) {
  document.querySelectorAll('.modal').forEach(function(modal) {
    if (event.target == modal) {
      modal.style.display = 'none';
    }
  });
};
