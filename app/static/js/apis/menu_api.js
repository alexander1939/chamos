document.addEventListener("DOMContentLoaded", () => {
    const menuList = document.getElementById("menu-list");
    const token = localStorage.getItem("token");

    if (token) {
        fetch("/api/menu", {
            method: "GET",
            headers: {
                Authorization: token,
            },
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.error) {
                    console.error("Error en API:", data.error);
                    return;
                }

                menuList.innerHTML = `<li><a href="/"><i class="fas fa-home"></i> Inicio</a></li>`;

                data.privilegios.forEach((privilegio) => {
                    const items = data.contenido[privilegio] || [];
                    menuList.innerHTML += createDropdown(privilegio, items);
                });
            })
            .catch((error) => console.error("Error al obtener el menú:", error));
    }
});

function createDropdown(title, items) {
    let dropdown = `
          <li>
              <a href="#" class="dropdown-btn">
                  <i class="fas fa-folder"></i> ${title} 
                  <i class="fas fa-chevron-down dropdown-icon"></i>
              </a>
              <ul class="dropdown-options" style="display: none;">
                  <li><a href="/${title.toLowerCase()}/agregar">
                      <i class="fas fa-plus-circle"></i> Agregar</a></li>
                  <li><a href="/${title.toLowerCase()}/listar">
                      <i class="fas fa-list"></i> Listar</a></li>
    `;

    items.forEach((item) => {
        dropdown += `<li><a href="#"><i class="fas fa-file-alt"></i> ${item.nombre}</a></li>`;
    });

    dropdown += "</ul></li>";
    return dropdown;
}
