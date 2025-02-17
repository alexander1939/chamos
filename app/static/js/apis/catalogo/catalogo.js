// catalogo.js

document.addEventListener("DOMContentLoaded", () => {
    // Verifica si estamos en una página de detalle
    const itemId = obtenerItemId();
    if (itemId) {
        return; // No inicializa el catálogo si estamos en una página de detalle
    }

    inicializarCatalogo(); // Inicializa los eventos de clic en los enlaces "Listar"

    const modulo = obtenerModulo();
    if (modulo) {
        cargarCatalogo(modulo); // Cargar catálogo si la URL ya es /catalogo/<modulo>/
    }

    // Manejar el evento de retroceso del navegador (para que no recargue todo)
    window.addEventListener("popstate", () => {
        const modulo = obtenerModulo();
        if (modulo) {
            cargarCatalogo(modulo);
        }
    });
});

// 🔹 Función para inicializar los eventos en los enlaces "Listar"
function inicializarCatalogo() {
    document.body.addEventListener("click", async (e) => {
        const link = e.target.closest(".list-link");
        if (link) {
            e.preventDefault(); // Evita la recarga completa de la página

            const modulo = link.getAttribute("data-modulo");
            if (modulo) {
                window.history.pushState({}, '', `/catalogo/${modulo}/`); // Actualiza la URL sin recargar
                await cargarCatalogo(modulo); // Cargar el contenido dinámicamente
            }
        }
    });
}

// 🔹 Función para obtener el módulo desde la URL
function obtenerModulo() {
    const pathSegments = window.location.pathname.split("/");
    return pathSegments[2] || null; // Obtiene el módulo de la URL (materias, proyectos, juegos)
}

// 🔹 Función para obtener datos del catálogo desde el backend
async function obtenerDatos(modulo) {
    try {
        const response = await fetch(`/api/catalogo/?modulo=${modulo}`, {
            method: "GET",
            credentials: "include"
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error("Error al obtener el catálogo:", error);
        return { error: "Error al conectar con el servidor." };
    }
}

// 🔹 Función para cargar el catálogo en el contenedor
async function cargarCatalogo(modulo) {
    if (!modulo) return;

    const contentContainer = document.getElementById("content-container");
    if (!contentContainer) {
        console.error("Error: No se encontró el #content-container en el DOM.");
        return;
    }

    try {
        contentContainer.innerHTML = `<p>Cargando ${modulo}...</p>`; // Mensaje de carga

        const data = await obtenerDatos(modulo);
        if (data.error) {
            mostrarError(data.error);
        } else {
            mostrarDatos(data, modulo);
        }
    } catch (error) {
        mostrarError("Error al cargar el catálogo.");
    }
}

// 🔹 Función para mostrar los datos en el DOM
function mostrarDatos(data, modulo) {
    const contentContainer = document.getElementById("content-container");
    contentContainer.innerHTML = ""; // Limpia el contenido previo

    if (!data || data.error || (!data.materias && !data.proyectos && !data.juegos)) {
        mostrarError("No se encontraron datos.");
        return;
    }

    const items = data.materias || data.proyectos || data.juegos;
    if (items.length === 0) {
        mostrarError("No hay registros disponibles.");
        return;
    }

    // Título y descripción dinámicos
    const titulo = document.createElement("h2");
    titulo.className = "display-4 text-primary text-center";
    titulo.textContent = `${modulo} Registrados`;

    const descripcion = document.createElement("p");
    descripcion.className = "lead text-muted text-center";
    descripcion.textContent = `Aquí puedes ver todos los ${modulo.toLowerCase()} registrados.`;

    contentContainer.appendChild(titulo);
    contentContainer.appendChild(descripcion);

    // Contenedor de tarjetas
    const cardContainer = document.createElement("div");
    cardContainer.className = "row row-cols-1 row-cols-md-3 g-4";
    contentContainer.appendChild(cardContainer);

    // Renderizar las tarjetas
    items.forEach(item => {
        cardContainer.appendChild(crearTarjeta(item, modulo, data));
    });

    // Botón de agregar si hay permisos
    if (data.can_create) {
        const addButton = document.createElement("a");
        addButton.href = `/catalogo/${modulo}/agregar/`;
        addButton.className = "btn btn-success btn-lg";
        addButton.textContent = `Agregar Nuevo ${modulo.slice(0, -1)}`;

        const addButtonContainer = document.createElement("div");
        addButtonContainer.className = "text-center mt-4";
        addButtonContainer.appendChild(addButton);

        contentContainer.appendChild(addButtonContainer);
    }
}

// 🔹 Función para crear una tarjeta de catálogo
function crearTarjeta(item, modulo, data) {
    const col = document.createElement("div");
    col.className = "col content-item";
    col.innerHTML = `
        <div class="card shadow-sm border-light rounded">
            <div class="card-body">
                <h5 class="card-title">${item.nombre}</h5>
                <p class="card-text">${item.descripcion}</p>
                <div class="d-flex justify-content-between align-items-center">
                    <a href="/catalogo/${modulo}/detalle/${item.id}" class="deta-link btn btn-primary btn-sm">Ver Detalles</a>
                    <div class="d-flex">
                        ${data.can_edit ? `
                        <a href="/catalogo/${modulo}/editar/${item.id}" class="btn btn-warning btn-sm me-2">
                            <img src="/static/images/edit.png" alt="Editar" width="20" height="20">
                        </a>` : ""}
                        ${data.can_delete ? `
 <button class="btn btn-danger btn-sm btn-eliminar" data-modulo="${modulo}" data-id="${item.id}">
    <img src="/static/images/delete.png" alt="Eliminar" width="20" height="20">
</button>
` : ""}
                    </div>
                </div>
            </div>
        </div>
    `;
    return col;
}

// 🔹 Función para mostrar errores
function mostrarError(error) {
    const contentContainer = document.getElementById("content-container");
    if (!contentContainer) {
        console.error("Error: No se encontró el elemento #content-container en el DOM.");
        return;
    }

    contentContainer.innerHTML = `<p style="color: red;">${error}</p>`;
}
