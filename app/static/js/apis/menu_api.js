document.addEventListener("DOMContentLoaded", function () {
    const menuList = document.getElementById("menu-list");

    const token = localStorage.getItem("token");  // Obtener el token del localStorage

    fetch("/menu/", {
        method: "GET",
        headers: {
            "Authorization": token  // Agregar el token al encabezado
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Error al obtener el menú:", data.error);
                return;
            }

            const { privilegios, contenido } = data;

            if (privilegios.includes("Proyectos")) {
                const proyectosMenu = `
                <li>
                    <a href="#"><i class="fas fa-folder"></i> Proyectos</a>
                    <ul>
                        ${contenido.Proyectos.map(proyecto => `<li><a href="#">${proyecto.nombre}</a></li>`).join("")}
                    </ul>
                </li>
            `;
                menuList.innerHTML += proyectosMenu;
            }

            if (privilegios.includes("Juegos")) {
                const juegosMenu = `
                <li>
                    <a href="#"><i class="fas fa-folder"></i> Juegos</a>
                    <ul>
                        ${contenido.Juegos.map(juego => `<li><a href="#">${juego.nombre}</a></li>`).join("")}
                    </ul>
                </li>
            `;
                menuList.innerHTML += juegosMenu;
            }

            if (privilegios.includes("Materias")) {
                const materiasMenu = `
                <li>
                    <a href="#"><i class="fas fa-folder"></i> Materias</a>
                    <ul>
                        ${contenido.Materias.map(materia => `<li><a href="#">${materia.nombre}</a></li>`).join("")}
                    </ul>
                </li>
            `;
                menuList.innerHTML += materiasMenu;
            }
        })
        .catch(error => console.error("Error al cargar el menú:", error));
});
