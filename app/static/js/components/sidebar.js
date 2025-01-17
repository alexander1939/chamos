// sidebar.js
document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById("sidebar");
    const toggleMenu = document.getElementById("toggle-menu");
    const closeMenu = document.getElementById("close-menu");
    const dropdownBtns = document.querySelectorAll(".dropdown-btn");
  
    // Mostrar menú al presionar el botón de hamburguesa
    toggleMenu.addEventListener("click", () => {
      sidebar.classList.add("active");
    });
  
    // Ocultar menú al presionar el botón de cerrar
    closeMenu.addEventListener("click", () => {
      sidebar.classList.remove("active");
    });
  
    // Activar o desactivar dropdowns
    dropdownBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        btn.classList.toggle("active");
      });
    });
  });
  