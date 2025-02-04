document.addEventListener("DOMContentLoaded", () => {
  const sidebar = document.getElementById("sidebar");
  const toggleMenu = document.getElementById("toggle-menu");
  const closeMenu = document.getElementById("close-menu");
  const menuList = document.getElementById("menu-list");

  // Mostrar menú al presionar el botón de hamburguesa
  toggleMenu.addEventListener("click", () => {
    sidebar.classList.add("active");
  });

  // Ocultar menú al presionar el botón de cerrar
  closeMenu.addEventListener("click", () => {
    sidebar.classList.remove("active");
  });

  // Delegación de eventos para manejar los desplegables
  menuList.addEventListener("click", (event) => {
    if (event.target.classList.contains("dropdown-btn")) {
      event.target.classList.toggle("active");

      // Buscar el siguiente elemento y alternar su visibilidad
      const dropdownOptions = event.target.nextElementSibling;
      if (dropdownOptions && dropdownOptions.classList.contains("dropdown-options")) {
        dropdownOptions.style.display =
          dropdownOptions.style.display === "block" ? "none" : "block";
      }
    }
  });
});
