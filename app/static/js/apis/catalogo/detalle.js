document.addEventListener("DOMContentLoaded", () => {
    // Verifica si estamos en la sección de usuarios
    if (estaEnUsuarios()) {
        obtenerUsuarios()
            .then(data => mostrarUsuarios(data))
            .catch(error => mostrarError(error));
    } else {
        // Si no estamos en la sección de usuarios, intenta obtener el detalle de un ítem
        const modulo = obtenerModulo();
        const itemId = obtenerItemId();
        if (!modulo || !itemId) return;

        obtenerDetalle(modulo, itemId)
            .then(data => mostrarDetalle(data, modulo))
            .catch(error => mostrarError(error));
    }
});

/*
   Verifica si el DOM ya ha sido cargado; si es así, ejecuta la función `iniciarUsuarios`.
   Si aún no está cargado, espera a que lo esté y luego ejecuta `iniciarUsuarios`.
*/

/*
   Esta función realiza el mismo proceso que el bloque anterior, 
   pero puede ser llamada en otros contextos si es necesario.
*/
function iniciarUsuarios() {
    if (!estaEnUsuarios()) return;  /* Verifica si estamos en la sección de usuarios */

    obtenerUsuarios()  /* Llama a la función para obtener usuarios */
        .then(data => mostrarUsuarios(data))  /* Muestra los usuarios obtenidos */
        .catch(error => mostrarError(error));  /* Muestra un error si ocurre */
}

/* 
   Esta función verifica si la página actual corresponde a la sección de usuarios 
   (ya sea en la ruta principal o en una ruta que comience con "/home").
*/
function estaEnUsuarios() {
    return window.location.pathname === "/" || window.location.pathname.startsWith("/home");
}

function obtenerModulo() {
    const pathSegments = window.location.pathname.split("/");
    return pathSegments[2] || null;
}

function obtenerItemId() {
    const pathSegments = window.location.pathname.split("/");
    return pathSegments[4] || null;
}

async function obtenerUsuarios() {
    const response = await fetch("/api/usuarios", {
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

function mostrarUsuarios(data) {
    const contentContainer = document.getElementById("content-container");
    contentContainer.innerHTML = "";

    if (!data || data.error) {
        mostrarError(data.error || "No se encontró información de usuarios.");
        return;
    }

    const usuarios = data.usuarios;

    // Crear el título y la descripción del módulo dinámicamente
    const titulo = document.createElement("h2");
    titulo.className = "display-4 text-primary text-center";
    titulo.textContent = "Usuarios";

    const descripcion = document.createElement("p");
    descripcion.className = "lead text-muted text-center";
    descripcion.textContent = "Aquí puedes ver la lista de usuarios.";

    // Crear un contenedor para las tarjetas de usuarios
    const cardContainer = document.createElement("div");
    cardContainer.className = "row row-cols-1 row-cols-md-3 g-4";
    contentContainer.appendChild(cardContainer);

    // Crear una tarjeta por cada usuario
    usuarios.forEach(usuario => {
        const col = document.createElement("div");
        col.className = "col content-item";
        col.innerHTML = `
            <div class="card shadow-sm border-light rounded">
                <div class="card-body">
                    <h5 class="card-title">${usuario.nombre}</h5>
                    <p class="card-text">${usuario.descripcion}</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <a href="/usuarios/${usuario.id}" class="btn btn-primary btn-sm">Ver Detalle</a>
                    </div>
                </div>
            </div>
        `;
        cardContainer.appendChild(col);
    });

    // Agregar el título y la descripción al contenedor
    contentContainer.appendChild(titulo);
    contentContainer.appendChild(descripcion);
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