// detalles.js

document.addEventListener("DOMContentLoaded", () => {
    inicializarDetalles(); // Inicializa los eventos de clic en los enlaces de detalles

    const modulo = obtenerModulo();
    const itemId = obtenerItemId();

    // Verifica si el servidor ya cargó la página con detalles
    const contenidoCargado = document.getElementById("content-container").dataset.cargado === "true";

    if (modulo && itemId && !contenidoCargado) {
        console.log(`Cargando detalles desde URL: modulo=${modulo}, itemId=${itemId}`);
        cargarDetalle(modulo, itemId); // Solo cargar si no está ya cargado por el servidor
    }

    // Maneja el botón "Atrás" del navegador sin recargar la página
    window.addEventListener("popstate", () => {
        const modulo = obtenerModulo();
        const itemId = obtenerItemId();
        if (modulo && itemId) {
            console.log(`Volviendo a detalles: modulo=${modulo}, itemId=${itemId}`);
            cargarDetalle(modulo, itemId);
        }
    });
});

// 🔹 Función para inicializar los eventos en los enlaces "Detalles"
function inicializarDetalles() {
    document.body.addEventListener("click", async (e) => {
        const link = e.target.closest(".deta-link");
        if (link) {
            e.preventDefault(); // Evita la recarga completa de la página

            const href = link.getAttribute("href");
            const partesURL = href.split("/");

            const modulo = partesURL[2]; // Extrae el nombre del módulo
            const itemId = partesURL[4]; // Extrae el itemId

            console.log(`Clic en detalle: modulo=${modulo}, itemId=${itemId}`);

            if (modulo && itemId) {
                window.history.pushState({}, '', `/catalogo/${modulo}/detalle/${itemId}/`); // Actualiza la URL sin recargar
                await cargarDetalle(modulo, itemId); // Carga los detalles dinámicamente
            }
        }
    });
}

// 🔹 Función para obtener el módulo desde la URL
function obtenerModulo() {
    const pathSegments = window.location.pathname.split("/");
    return pathSegments[2] || null;
}

// 🔹 Función para obtener el itemId desde la URL
function obtenerItemId() {
    const pathSegments = window.location.pathname.split("/");
    return pathSegments[4] || null;
}

// 🔹 Función para obtener los detalles del ítem desde el backend
async function obtenerDetalle(modulo, itemId) {
    try {
        console.log(`Obteniendo detalle del backend: modulo=${modulo}, itemId=${itemId}`);

        const response = await fetch(`/api/catalogo/detalle/?modulo=${modulo}&id=${itemId}`, {
            method: "GET",
            credentials: "include"
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error("Error al obtener el detalle:", error);
        return { error: "Error al conectar con el servidor." };
    }
}

// 🔹 Función para cargar los detalles en el contenedor
async function cargarDetalle(modulo, itemId) {
    if (!modulo || !itemId) {
        console.error("Falta el módulo o itemId");
        return;
    }

    const contentContainer = document.getElementById("content-container");
    if (!contentContainer) {
        console.error("Error: No se encontró el #content-container en el DOM.");
        return;
    }

    try {
        contentContainer.innerHTML = `<p>Cargando detalle...</p>`; // Mensaje de carga

        const data = await obtenerDetalle(modulo, itemId);
        if (data.error) {
            mostrarError(data.error);
        } else {
            mostrarDetalle(data, modulo);
        }
    } catch (error) {
        mostrarError("Error al cargar los detalles.");
    }
}

// 🔹 Función para mostrar los detalles en el DOM
function mostrarDetalle(data, modulo) {
    const contentContainer = document.getElementById("content-container");
    contentContainer.innerHTML = ""; // Limpia el contenido previo

    if (!data || data.error) {
        mostrarError("No se encontraron detalles.");
        return;
    }

    const detalle = data.detalle;

    console.log("Mostrando detalle en el DOM:", detalle);

    // Marcar que el contenido ya fue cargado
    contentContainer.dataset.cargado = "true";

    // Crear el título y la descripción dinámicamente
    const titulo = document.createElement("h2");
    titulo.className = "display-4 text-primary text-center";
    titulo.textContent = `Detalle de ${detalle.nombre}`;

    const descripcion = document.createElement("p");
    descripcion.className = "lead text-muted text-center";
    descripcion.textContent = `Aquí puedes ver los detalles de ${detalle.nombre}.`;

    // Contenedor de la tarjeta de detalles
    const cardContainer = document.createElement("div");
    cardContainer.className = "row row-cols-1 row-cols-md-3 g-4";
    contentContainer.appendChild(cardContainer);

    // Crear la tarjeta de detalles
    const col = document.createElement("div");
    col.className = "col content-item";
    col.innerHTML = `
        <div class="card shadow-sm border-light rounded">
            <div class="card-body">
                <h5 class="card-title">${detalle.nombre}</h5>
                <p class="card-text">${detalle.descripcion}</p>
                <div class="d-flex justify-content-between align-items-center">
                    <a href="/catalogo/${modulo}/" class="btn btn-primary btn-sm">Volver al Catálogo</a>
                </div>
            </div>
        </div>
    `;

    // Agregar elementos al contenedor
    contentContainer.appendChild(titulo);
    contentContainer.appendChild(descripcion);
    cardContainer.appendChild(col);
}

// 🔹 Función para mostrar errores en el contenedor
function mostrarError(error) {
    const contentContainer = document.getElementById("content-container");
    if (!contentContainer) {
        console.error("Error: No se encontró el elemento #content-container en el DOM.");
        return;
    }
    contentContainer.innerHTML = `<p style="color: red;">${error}</p>`;
}
