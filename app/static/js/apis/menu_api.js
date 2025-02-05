document.addEventListener("DOMContentLoaded", async () => {
    const menuList = document.getElementById("menu-list");

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

        menuList.innerHTML = `<li><a href="/"><i class="fas fa-home"></i> Inicio</a></li>`;

        if (!data.contenido || Object.keys(data.contenido).length === 0) {
            console.warn("El usuario no tiene contenido asignado.");
            return;
        }

        data.privilegios.forEach((privilegeName) => {
            const moduleData = data.contenido[privilegeName] || {};
            const items = moduleData.items || [];
            const canCreate = moduleData.can_create || false;
            const canView = moduleData.can_view || false;

            menuList.innerHTML += createDropdown(privilegeName, items, canCreate, canView);
        });

    } catch (error) {
        console.error("Error al conectar con la API del menú:", error);
        alert("No se pudo cargar el menú. Verifica tu conexión e intenta nuevamente.");
    }
});

const privilegeRoutes = {
    "Materias": "/gestion/materias",
    "Juegos": "/gestion/juegos",
    "Proyectos": "/gestion/proyectos",
    "Gestionar Privilegios": "/gestionar_privilegios/"
};

function createDropdown(privilegeName, items, canCreate, canView) {
    let dropdown = `
        <li>
            <a href="#" class="dropdown-btn">
                <i class="fas fa-folder"></i> ${privilegeName} 
                <i class="fas fa-chevron-down dropdown-icon"></i>
            </a>
            <ul class="dropdown-options" style="display: none;">
    `;

    const listRoute = privilegeRoutes[privilegeName] || `/${privilegeName.toLowerCase()}/listar`;
    const addRoute = privilegeRoutes[privilegeName] ? `${privilegeRoutes[privilegeName]}/agregar` : `/${privilegeName.toLowerCase()}/agregar`;

    if (canCreate) {
        dropdown += `
            <li><a href="${addRoute}">
                <i class="fas fa-plus-circle"></i> Agregar</a></li>
        `;
    }

    if (canView) {
        dropdown += `
            <li><a href="${listRoute}">
                <i class="fas fa-list"></i> Listar</a></li>
        `;
    }

    if (Array.isArray(items) && items.length > 0) {
        items.forEach((item) => {
            dropdown += `<li><a href="#"><i class="fas fa-file-alt"></i> ${item.nombre || item.name}</a></li>`;
        });
    } else {
        dropdown += `<li><span class="no-items">No hay elementos disponibles</span></li>`;
    }

    dropdown += `</ul></li>`;
    return dropdown;
}
