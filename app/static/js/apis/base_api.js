
/*
Inicializa la carga de datos del menú:
1. Verifica si el menú ya ha sido cargado mediante el atributo "data-loaded".
2. Si no ha sido cargado, llama a la función para cargar los datos.
*/

document.addEventListener("DOMContentLoaded", async () => {
    const menuList = document.getElementById("menu-list");

    if (!menuList.dataset.loaded) {
        await cargarDatos();
        menuList.dataset.loaded = "true";
    }
});



/*
Función que carga los datos del menú desde la API:
1. Realiza una petición GET a la API para obtener los datos del menú y privilegios.
2. Si la respuesta es válida, procesa y muestra los datos del menú.
3. Si ocurre un error, maneja el error adecuadamente (redirige al login o muestra un mensaje).
*/
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
                window.location.href = "/login";
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

        actualizarNombreUsuario(data.usuario);
        cargarMenu(data.menu, data.privilegios);
        actualizarSelect(data.menu, data.privilegios);
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
        userNameElement.textContent = usuario.name || "Usuario desconocido";
    }
}

/*
Carga y genera el menú de navegación dinámicamente:
1. Itera sobre los módulos disponibles en el menú.
2. Muestra los módulos y las opciones según los privilegios del usuario.
3. Para cada módulo, genera un dropdown con las opciones correspondientes (agregar, listar, detalles).
*/
function cargarMenu(menu, privilegios) {
    const menuList = document.getElementById("menu-list");
    if (!menuList) return;

    menuList.innerHTML = `<li><a href="/"class="home-link"><i class="fas fa-home"></i> Inicio</a></li>`;

    if (!Array.isArray(menu) || menu.length === 0) {
        console.warn("No hay módulos en el menú.");
        return;
    }

    menu.forEach(modulo => {
        if (!privilegios.includes(modulo.nombre)) return;

        const { nombre, contenido, can_create, can_view } = modulo;
        menuList.innerHTML += createDropdown(nombre, contenido, can_create, can_view);
    });

    activarDropdowns();
}

/*
Crea el dropdown de un módulo con sus opciones (agregar, listar, detalles):
1. Crea un elemento de lista con un enlace que muestra/oculta las opciones.
2. Agrega enlaces para agregar, listar y ver detalles de los elementos.
3. Si no hay elementos, muestra un mensaje indicando que no hay elementos disponibles.
*/
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
        dropdown += `<li><a href="/catalogo/agregar/${nombre}/" class="btn-agregar" data-modulo="${nombre}"><i class="fas fa-plus-circle"></i> Agregar</a></li>`;
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

/*
Activa la funcionalidad de los botones de dropdown:
1. Al hacer clic en el botón de un dropdown, muestra u oculta el submenú correspondiente.
*/
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

/*
Actualiza las opciones del select de categorías:
1. Agrega opciones al select basándose en los módulos disponibles y los privilegios del usuario.
2. La opción "todos" se agrega por defecto.
*/
function actualizarSelect(menu, privilegios) {
    const selectElement = document.getElementById("category-select");
    if (!selectElement) return;

    selectElement.innerHTML = `
        <option value="" disabled selected>Selecciona una categoría...</option>
        <option value="todos">Todos</option>
    `;

    menu.forEach(modulo => {
        if (privilegios.includes(modulo.nombre)) {
            const option = document.createElement("option");
            option.value = modulo.nombre;
            option.textContent = modulo.nombre;
            selectElement.appendChild(option);
        }
    });
}