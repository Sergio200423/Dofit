// ===== FUNCIONALIDAD DEL MODAL DE PERFIL - VERSIÓN CORREGIDA =====
document.addEventListener("DOMContentLoaded", () => {
  console.log("Inicializando modal de perfil...")

  // Elementos del modal
  var profileModal = document.getElementById("profileModal")
  var closeBtn = document.querySelector(".profile-modal-close")
  var cancelBtn = document.getElementById("cancelProfile")
  var saveBtn = document.getElementById("saveProfile")
  var profileNameInput = document.getElementById("profileName")
  var avatarOptions = document.querySelectorAll(".avatar-option")

  // Elementos del sidebar para actualizar
  var sidebarUserName = document.querySelector(".sidebar-user__title")
  var sidebarUserImg = document.querySelector(".sidebar-user-img img")
  var navUserImg = document.querySelector(".nav-user-img img")

  // Variables para almacenar la selección
  var selectedAvatar = localStorage.getItem("userAvatar") || "avatar-illustrated-02"
  var currentUserName = localStorage.getItem("userName") || "Nafisa Sh."

  // Variable Swal declaration
  console.log("Swal en perfil.js:", typeof Swal);
  console.log("Modal encontrado:", !!profileModal)
  console.log("Avatar actual:", selectedAvatar)
  console.log("Nombre actual:", currentUserName)

  // Inicializar perfil al cargar la página
  function initializeProfile() {
    if (sidebarUserName) sidebarUserName.textContent = currentUserName
    updateAvatarImages(selectedAvatar)
  }

  // Actualizar imágenes de avatar
  function updateAvatarImages(avatarName) {
    // Usar la ruta y nombres de avatar del modal
    var avatarPath = "/static/common/img/avatares/user-" + avatarName.split("-").pop() + ".jpg";
    if (sidebarUserImg) sidebarUserImg.src = avatarPath
    if (navUserImg) navUserImg.src = avatarPath
  }

  // Abrir modal
  function openProfileModal() {
    console.log("Abriendo modal de perfil...")
    if (profileModal) {
      profileModal.classList.add("show")
      if (profileNameInput) {
        profileNameInput.value = currentUserName
      }

      // Marcar avatar seleccionado
      avatarOptions.forEach((option) => {
        option.classList.remove("selected")
        if (option.dataset.avatar === selectedAvatar) {
          option.classList.add("selected")
        }
      })

      // Cerrar dropdown del usuario
      var userDropdown = document.querySelector(".nav-user-dropdown")
      var layer = document.querySelector(".layer")
      if (userDropdown) userDropdown.classList.remove("active")
      if (layer) layer.classList.remove("active")
    }
  }

  // Cerrar modal
  function closeProfileModal() {
    console.log("Cerrando modal de perfil...")
    if (profileModal) {
      profileModal.classList.remove("show")
    }
  }

  // Guardar cambios
  function saveProfile() {
    var newName = profileNameInput.value.trim()
    var selectedAvatarOption = document.querySelector(".avatar-option.selected")

    if (newName === "") {
      if (typeof Swal !== "undefined") {
        console.log("Voy a mostrar Swal.fire: nombre inválido");
        Swal.fire({
          title: "Nombre inválido",
          text: "Por favor ingresa un nombre válido",
          icon: "warning",
          timer: 2000,
          showConfirmButton: false,
        });
      }
      return;
    }

    if (!selectedAvatarOption) {
      if (typeof Swal !== "undefined") {
        console.log("Voy a mostrar Swal.fire: selecciona avatar");
        Swal.fire({
          title: "Selecciona un avatar",
          text: "Por favor selecciona un avatar",
          icon: "warning",
          timer: 2000,
          showConfirmButton: false,
        });
      }
      return;
    }

    // Actualizar variables
    currentUserName = newName
    selectedAvatar = selectedAvatarOption.dataset.avatar

    // Guardar en localStorage
    localStorage.setItem("userName", currentUserName)
    localStorage.setItem("userAvatar", selectedAvatar)

    // Actualizar interfaz
    if (sidebarUserName) sidebarUserName.textContent = currentUserName
    updateAvatarImages(selectedAvatar)

    // Cerrar modal
    closeProfileModal()

    // Mostrar confirmación
    if (typeof Swal !== "undefined") {
      console.log("Voy a mostrar Swal.fire: perfil actualizado");
      Swal.fire({
        title: "¡Perfil actualizado!",
        text: "Los cambios se han guardado correctamente",
        icon: "success",
        timer: 2000,
        showConfirmButton: false,
      });
    }
  }

  // Buscar el botón de perfil de manera más específica
  function findProfileButton() {
    var userDropdown = document.querySelector(".nav-user-dropdown");
    if (userDropdown) {
      var profileLinks = userDropdown.querySelectorAll("a");
      for (var i = 0; i < profileLinks.length; i++) {
        var link = profileLinks[i];
        var icon = link.querySelector('i[data-feather="user"]');
        if (icon) {
          console.log("Botón de perfil encontrado (en dropdown)");
          return link;
        }
      }
    }
    return null;
  }

  // Event listeners
  var profileBtn = document.getElementById("btn-perfil");
  if (profileBtn) {
    profileBtn.addEventListener("click", (e) => {
      e.preventDefault();
      openProfileModal();
    });
  } else {
    console.log("No se encontró el botón de perfil");
  }

  if (closeBtn) {
    closeBtn.addEventListener("click", closeProfileModal)
  }

  if (cancelBtn) {
    cancelBtn.addEventListener("click", closeProfileModal)
  }

  if (saveBtn) {
    saveBtn.addEventListener("click", saveProfile)
  }

  // Selección de avatar
  avatarOptions.forEach((option) => {
    option.addEventListener("click", function () {
      avatarOptions.forEach((opt) => {
        opt.classList.remove("selected")
      })
      this.classList.add("selected")
    })
  })

  // Cerrar modal al hacer clic fuera
  if (profileModal) {
    profileModal.addEventListener("click", (e) => {
      if (e.target === profileModal) {
        closeProfileModal()
      }
    })
  }

  // Cerrar modal con tecla Escape
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && profileModal && profileModal.classList.contains("show")) {
      closeProfileModal()
    }
  })

  // Inicializar perfil
  initializeProfile()
})
