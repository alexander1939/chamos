document.addEventListener("DOMContentLoaded", () => {
    const modulo = obtenerModulo();
    const itemId = obtenerItemId();
    if (!modulo || !itemId) return;

    obtenerDetalle(modulo, itemId)
        .then(data => mostrarDetalle(data, modulo))
        .catch(error => mostrarError(error));
});

function obtenerModulo() {
    const pathSegments = window.location.pathname.split("/");
    return pathSegments[2] || null;
}

function obtenerItemId() {
    const pathSegments = window.location.pathname.split("/");
    return pathSegments[4] || null;
}

async function obtenerDetalle(modulo, itemId) {
    const response = await fetch(`/api/catalogo/detalle/?modulo=${modulo}&id=${itemId}`, {
        method: "GET",
        credentials: "include", // Para enviar cookies si es necesario
        headers: {
            "Content-Type": "application/json"
        }
    });

    if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
    }

    return response.json();
}

function mostrarDetalle(data, modulo) {
    const contentContainer = document.getElementById("content-container");
    contentContainer.innerHTML = "";

    if (!data || data.error) {
        mostrarError(data.error || "No se encontró información del detalle.");
        return;
    }

    const detalle = data.detalle;

    // Crear el título y la descripción del módulo dinámicamente
    const titulo = document.createElement("h2");
    titulo.className = "display-4 text-primary text-center";
    titulo.textContent = `${modulo} - Detalle`;

    const descripcion = document.createElement("p");
    descripcion.className = "lead text-muted text-center";
    descripcion.textContent = `Aquí puedes ver los detalles del ${modulo.toLowerCase()}.`;

    // Crear un contenedor para la tarjeta de detalles
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
                    <a href="/catalogo/${modulo}" class="btn btn-primary btn-sm">Volver al Catálogo</a>
                </div>
            </div>
        </div>
    `;

    // Agregar el título, la descripción y la tarjeta al contenedor
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