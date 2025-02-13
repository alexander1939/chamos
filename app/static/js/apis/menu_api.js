document.addEventListener("DOMContentLoaded", async () => {
    await cargarDatos();
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
                window.location.href = "/login";
            } else {
                console.error(`Error en la API (Código ${response.status}): ${response.statusText}`);
            }
            return;
        }

        const data = await response.json();

        if (!data || typeof data !== "object") {
            console.error("La API devolvió un formato inesperado:", data);
            return;
        }

        if (data.error) {
            console.error("Error en la API:", data.error);
            return;
        }

        // Mostrar nombre del usuario
        actualizarNombreUsuario(data.usuario);

        // Cargar el menú
        cargarMenu(data.menu, data.privilegios);

        // Actualizar el select con las categorías basadas en los privilegios
        actualizarSelect(data.menu, data.privilegios);
    } catch (error) {
        console.error("Error al conectar con la API del menú:", error);
    }
}

// 🔹 **Actualiza el nombre del usuario en la interfaz**
function actualizarNombreUsuario(usuario) {
    const userNameElement = document.getElementById("user-name");
    if (usuario && userNameElement) {
        userNameElement.textContent = usuario.name || "Usuario desconocido";
    }
}

// 🔹 **Carga el menú en la interfaz**
function cargarMenu(menu, privilegios) {
    const menuList = document.getElementById("menu-list");
    if (!menuList) return;

    menuList.innerHTML = `<li><a href="/"><i class="fas fa-home"></i> Inicio</a></li>`;

    if (!Array.isArray(menu) || menu.length === 0) {
        console.warn("No hay módulos en el menú.");
        return;
    }

    menu.forEach(modulo => {
        if (!privilegios.includes(modulo.nombre)) return; // Si no está en privilegios, ignorarlo

        const { nombre, contenido, can_create, can_view } = modulo;
        menuList.innerHTML += createDropdown(nombre, contenido, can_create, can_view);
    });

    // Habilitar funcionalidad de dropdowns
    activarDropdowns();
}

// 🔹 **Crea el menú desplegable**
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
        dropdown += `<li><a href="/catalogo/${nombre}/agregar/"><i class="fas fa-plus-circle"></i> Agregar</a></li>`;
    }

    if (canView) {
        dropdown += `<li><a href="/catalogo/${nombre}/"><i class="fas fa-list"></i> Listar</a></li>`;
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

// 🔹 **Activa los dropdowns del menú**
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

// 🔹 **Actualiza el select con las categorías basadas en los privilegios**
function actualizarSelect(menu, privilegios) {
    const selectElement = document.getElementById("category-select");
    if (!selectElement) return;

    // Limpiar el select
    selectElement.innerHTML = '<option value="" disabled selected>Selecciona una categoría...</option>';

    // Filtrar las categorías basadas en los privilegios
    menu.forEach(modulo => {
        if (privilegios.includes(modulo.nombre)) {
            const option = document.createElement("option");
            option.value = modulo.nombre;
            option.textContent = modulo.nombre;
            selectElement.appendChild(option);
        }
    });
}