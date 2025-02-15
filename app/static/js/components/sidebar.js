document.addEventListener("DOMContentLoaded", () => {
  console.log("Sidebar.js cargado"); // Verifica si el script se carga

  const sidebar = document.getElementById("sidebar");
  const toggleMenu = document.getElementById("toggle-menu");
  const closeMenu = document.getElementById("close-menu");

  if (!sidebar || !toggleMenu || !closeMenu) {
    console.error("Elementos del menú no encontrados.");
    return;
  }

  toggleMenu.addEventListener("click", () => {
    console.log("Botón de hamburguesa presionado");
    sidebar.classList.add("active");
  });

  closeMenu.addEventListener("click", () => {
    console.log("Botón de cerrar presionado");
    sidebar.classList.remove("active");
  });
});
