/*
    Este bloque de código se ejecuta cuando el contenido del DOM ha sido completamente cargado. 
    Primero, se obtiene el elemento del menú mediante `getElementById` y se verifica si los datos ya fueron cargados mediante el atributo `data-loaded`.
    Si los datos aún no han sido cargados, se llama a la función `cargarDatos()` de manera asincrónica. 
    Después de que los datos son cargados, se marca el atributo `data-loaded` como "true".
    Finalmente, se activa la navegación con la función `activarNavegacion()`, que permite el comportamiento dinámico de la navegación.
*/
document.addEventListener("DOMContentLoaded", async () => {
    const menuList = document.getElementById("menu-list");

    if (!menuList.dataset.loaded) {
        await cargarDatos(); // Espera a cargar los datos antes de marcar como cargado.
        menuList.dataset.loaded = "true"; // Marca los datos como cargados.
    }

});

/*
    La función `cargarDatos` obtiene información del servidor sobre el menú, los privilegios y el usuario. 
    Utiliza `fetch` para hacer una solicitud HTTP GET al endpoint "/api/menu". 
    Si la respuesta es exitosa, se procesa la información y se actualizan las secciones correspondientes de la página, 
    como el nombre del usuario, el menú y el selector de categorías.
    Si la respuesta no es exitosa, se maneja el error según el código de estado (401 si la sesión ha expirado, u otros códigos de error de la API).
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

/*
    La función `cargarMenu` es responsable de cargar el menú de navegación. 
    Primero, se limpia el contenido actual del menú y se añade un enlace de inicio.
    Luego, verifica que el menú recibido sea válido y lo recorre. 
    Para cada módulo en el menú, comprueba si el usuario tiene los privilegios necesarios para verlo, 
    y si es así, se agrega un ítem de menú con las opciones correspondientes.
    Si no se tienen privilegios para un módulo, se omite.
*/
function cargarMenu(menu, privilegios) {
    const menuList = document.getElementById("menu-list");
    if (!menuList) return;

    menuList.innerHTML = `<li><a href="/"class="nav-link"><i class="fas fa-home"></i> Inicio</a></li>`; // Agrega el ítem de inicio al menú.

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

/*
    La función `createDropdown` genera el HTML para un dropdown de navegación, basado en las opciones del menú.
    Para cada módulo, se verifica si el usuario tiene permisos para crear o ver contenido y se añaden las opciones correspondientes al dropdown.
    Si el módulo tiene subcontenido (como elementos de catálogo), se añaden enlaces a estos elementos. 
    Si no hay contenido disponible, se muestra un mensaje indicando que no hay elementos.
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
        dropdown += `<li><a href="/catalogo/${nombre}/agregar/"class="nav-link" ><i class="fas fa-plus-circle"></i> Agregar</a></li>`;
    }

    if (canView) {
        dropdown += `<li><a href="/catalogo/${nombre}/"class="nav-link"><i class="fas fa-list"></i> Listar</a></li>`;
    }

    if (Array.isArray(contenido) && contenido.length > 0) {
        contenido.forEach(item => {
            dropdown += `<li><a href="/catalogo/${nombre}/detalle/${item.id}">
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
    La función `activarDropdowns` permite la funcionalidad de mostrar u ocultar las opciones de cada dropdown cuando se hace clic en el encabezado del dropdown.
    Al hacer clic, si el submenu está oculto, se muestra; si está visible, se oculta.
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
    La función `actualizarSelect` llena un elemento `<select>` con las categorías disponibles en el menú, basándose en los privilegios del usuario.
    Para cada módulo del menú que el usuario puede ver, se crea una opción en el select con el nombre del módulo.
*/
function actualizarSelect(menu, privilegios) {
    const selectElement = document.getElementById("category-select");
    if (!selectElement) return;

    selectElement.innerHTML = '<option value="" disabled selected>Selecciona una categoría...</option>';

    menu.forEach(modulo => {
        if (privilegios.includes(modulo.nombre)) {
            const option = document.createElement("option");
            option.value = modulo.nombre;
            option.textContent = modulo.nombre;
            selectElement.appendChild(option);
        }
    });
}
