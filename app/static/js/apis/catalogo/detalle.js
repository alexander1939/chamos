
document.addEventListener("DOMContentLoaded", () => {
    inicializarDetalles();


    const modulo = obtenerModulo();
    const itemId = obtenerItemId();
    const esModoEdicion = window.location.pathname.includes("editar");

    if (modulo && itemId && !esModoEdicion) {
        console.log(`Cargando detalles desde URL: modulo=${modulo}, itemId=${itemId}`);
        cargarDetalle(modulo, itemId);
        actualizarBreadcrumbs();

    }
});


function inicializarDetalles() {
    document.body.addEventListener("click", async (e) => {
        const link = e.target.closest(".deta-link");
        if (link) {
            e.preventDefault();

            const href = link.getAttribute("href");
            const partesURL = href.split("/");

            const modulo = partesURL[2];
            const itemId = partesURL[4];

            console.log(`Clic en detalle: modulo=${modulo}, itemId=${itemId}`);

            if (modulo && itemId) {
                window.history.pushState({}, '', `/catalogo/${modulo}/detalle/${itemId}/`);
                await cargarDetalle(modulo, itemId);
                actualizarBreadcrumbs();
            }
        }
    });
}

// 🔹 Función para obtener el módulo desde la URL
function obtenerModulo() {
    const pathSegments = window.location.pathname.split("/");
    return pathSegments[2] || null;
}

function obtenerItemId() {
    const pathSegments = window.location.pathname.split("/");
    return pathSegments[4] || null;
}

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
        contentContainer.innerHTML = `<p>Cargando detalle...</p>`;

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

function mostrarDetalle(data, modulo) {
    const contentContainer = document.getElementById("content-container");
    contentContainer.innerHTML = "";

    if (!data || data.error) {
        mostrarError("No se encontraron detalles.");
        return;
    }

    const detalle = data.detalle;

    console.log("Mostrando detalle en el DOM:", detalle);

    contentContainer.dataset.cargado = "true";

    const titulo = document.createElement("h2");
    titulo.className = "display-4 text-primary text-center";
    titulo.textContent = `Detalle de ${detalle.nombre}`;

    const descripcion = document.createElement("p");
    descripcion.className = "lead text-muted text-center";
    descripcion.textContent = `Aquí puedes ver los detalles de ${detalle.nombre}.`;

    const cardContainer = document.createElement("div");
    cardContainer.className = "row row-cols-1 row-cols-md-3 g-4";
    contentContainer.appendChild(cardContainer);

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

    contentContainer.appendChild(titulo);
    contentContainer.appendChild(descripcion);
    cardContainer.appendChild(col);
}

function mostrarError(error) {
    const contentContainer = document.getElementById("content-container");
    if (!contentContainer) {
        console.error("Error: No se encontró el elemento #content-container en el DOM.");
        return;
    }
    contentContainer.innerHTML = `<p style="color: red;">${error}</p>`;
}
