
document.addEventListener("DOMContentLoaded", async () => {
    const menuList = document.getElementById("menu-list");

    if (!menuList.dataset.loaded) {
        await cargarDatos(); // Espera a cargar los datos antes de marcar como cargado.
        menuList.dataset.loaded = "true"; // Marca los datos como cargados.
    }

});

async function cargarDatos() {
    try {
        const response = await fetch("/api/menu", {
            method: "GET",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
        });

        if (!response.ok) {
            if (response.status === 401) {
                console.warn("Sesión expirada o token inválido. Redirigiendo a login...");
                window.location.href = "/login"; // Redirige al login si la sesión expira.
            } else {
                console.error(`Error en la API (Código ${response.status}): ${response.statusText}`);
            }
            return;
        }

        const data = await response.json();

        // Verifica que los datos recibidos sean válidos.
        if (!data || typeof data !== "object") {
            console.error("La API devolvió un formato inesperado:", data);
            return;
        }

        if (data.error) {
            console.error("Error en la API:", data.error);
            return;
        }

        actualizarNombreUsuario(data.usuario); // Actualiza el nombre del usuario.
        cargarMenu(data.menu, data.privilegios); // Carga el menú con los privilegios del usuario.
        actualizarSelect(data.menu, data.privilegios); // Actualiza el selector de categorías.
    } catch (error) {
        console.error("Error al conectar con la API del menú:", error);
    }
}

/*
    La función `actualizarNombreUsuario` actualiza el nombre del usuario en la interfaz de usuario.
    Si se recibe un nombre de usuario válido, se muestra. Si no, se muestra "Usuario desconocido".
*/
function actualizarNombreUsuario(usuario) {
    const userNameElement = document.getElementById("user-name");
    if (usuario && userNameElement) {
        userNameElement.textContent = usuario.name || "Usuario desconocido"; // Establece el nombre del usuario.
    }
}

function cargarMenu(menu, privilegios) {
    const menuList = document.getElementById("menu-list");
    if (!menuList) return;

    menuList.innerHTML = `<li><a href="/"class="home-link"><i class="fas fa-home"></i> Inicio</a></li>`; // Agrega el ítem de inicio al menú.

    if (!Array.isArray(menu) || menu.length === 0) {
        console.warn("No hay módulos en el menú.");
        return;
    }

    menu.forEach(modulo => {
        if (!privilegios.includes(modulo.nombre)) return; // Omite módulos sin privilegios.

        const { nombre, contenido, can_create, can_view } = modulo;
        menuList.innerHTML += createDropdown(nombre, contenido, can_create, can_view); // Crea el dropdown para cada módulo.
    });

    activarDropdowns(); // Activa el comportamiento de los dropdowns.
}

function createDropdown(nombre, contenido, canCreate, canView) {
    let dropdown = `
        <li>
            <a href="#" class="dropdown-btn">
                <i class="fas fa-folder"></i> ${nombre} 
                <i class="fas fa-chevron-down dropdown-icon"></i>
            </a>
            <ul class="dropdown-options" style="display: none;">
                        <li><a href="/contact" class="nav-link">Contacto</a></li>
    `;

    if (canCreate) {
        dropdown += `<li><a href="/catalogo/${nombre}/agregar/" ><i class="fas fa-plus-circle"></i> Agregar</a></li>`;
    }

    if (canView) {
        dropdown += `<li><a href="/catalogo/${nombre}/" class="list-link" data-modulo="${nombre}"><i class="fas fa-list"></i> Listar</a></li>`;
    }

    if (Array.isArray(contenido) && contenido.length > 0) {
        contenido.forEach(item => {
            dropdown += `<li><a href="/catalogo/${nombre}/detalle/${item.id}/" class="deta-link" >
                            <i class="fas fa-file-alt"></i> ${item.nombre}
                         </a></li>`;
        });
    } else {
        dropdown += `<li><span class="no-items">No hay elementos disponibles</span></li>`;
    }

    dropdown += `</ul></li>`;
    return dropdown;
}


function activarDropdowns() {
    document.querySelectorAll(".dropdown-btn").forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.preventDefault();
            const submenu = this.nextElementSibling;
            if (submenu.style.display === "none") {
                submenu.style.display = "block";
            } else {
                submenu.style.display = "none";
            }
        });
    });
}

function actualizarSelect(menu, privilegios) {
    const selectElement = document.getElementById("category-select");
    if (!selectElement) return;

    // Limpia el select y agrega la opción inicial y la opción "Todos".
    selectElement.innerHTML = `
        <option value="" disabled selected>Selecciona una categoría...</option>
        <option value="todos">Todos</option>
    `;

    // Recorre el menú y agrega las opciones según los privilegios.
    menu.forEach(modulo => {
        if (privilegios.includes(modulo.nombre)) {
            const option = document.createElement("option");
            option.value = modulo.nombre;
            option.textContent = modulo.nombre;
            selectElement.appendChild(option);
        }
    });
}
