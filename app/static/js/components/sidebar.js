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
    let target = event.target;
  
    // Verificar si el clic fue en el ícono y obtener el botón padre
    if (target.classList.contains("dropdown-icon")) {
      target = target.closest(".dropdown-btn"); // Busca el <a> más cercano
    }
  
    // Si el clic fue en el botón o su ícono, alternar el submenú
    if (target && target.classList.contains("dropdown-btn")) {
      target.classList.toggle("active");
  
      const dropdownOptions = target.nextElementSibling;
      if (dropdownOptions && dropdownOptions.classList.contains("dropdown-options")) {
        dropdownOptions.style.display =
          dropdownOptions.style.display === "block" ? "none" : "block";
      }
    }
  });
  
});

