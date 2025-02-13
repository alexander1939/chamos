document.addEventListener("DOMContentLoaded", () => {
    const modulo = obtenerModulo();
    if (!modulo) return;

    obtenerDatos(modulo)
        .then(data => mostrarDatos(data, modulo))
        .catch(error => mostrarError(error));
});

function obtenerModulo() {
    const pathSegments = window.location.pathname.split("/");
    return pathSegments[2] || null;  // Asumiendo que el módulo está en la 3ra parte de la URL
}

async function obtenerDatos(modulo) {
    const response = await fetch(`/api/catalogo/?modulo=${modulo}`, {
        method: "GET",
        credentials: "include"
    });

    if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
    }

    return response.json();
}

function mostrarDatos(data, modulo) {
    const contentContainer = document.getElementById("content-container");
    contentContainer.innerHTML = "";  // Limpiar contenido previo

    // Verificar si hay datos o si hay error
    if (!data || data.error || !data.materias && !data.proyectos && !data.juegos) {
        mostrarError("No tienes proyectos registrados.");
        return;
    }

    const items = data.materias || data.proyectos || data.juegos;
    if (items.length === 0) {
        mostrarError("No tienes proyectos registrados.");
        return;
    }

    // Crear y agregar tarjetas de datos
    items.forEach(item => {
        contentContainer.appendChild(crearTarjeta(item, modulo, data));
    });
}

function crearTarjeta(item, modulo, data) {
    const col = document.createElement("div");
    col.className = "col content-item";
    col.innerHTML = `
        <div class="card shadow-sm border-light rounded">
            <div class="card-body">
                <h5 class="card-title">${item.nombre}</h5>
                <p class="card-text">${item.descripcion}</p>
                <div class="d-flex justify-content-between align-items-center">
                    <a href="/catalogo/${modulo}/${item.id}" class="btn btn-primary btn-sm">Ver Detalles</a>
                    <div class="d-flex">
                        ${data.can_edit ? `
                        <a href="#" class="btn btn-warning btn-sm me-2">
                            <img src="/static/images/edit.png" alt="Editar" width="20" height="20">
                        </a>` : ""}
                        ${data.can_delete ? `
                        <form action="/catalo/eliminar/${modulo}/${item.id}" method="POST" style="display:inline-block;">
                            <button type="submit" class="btn btn-danger btn-sm">
                                <img src="/static/images/delete.png" alt="Eliminar" width="20" height="20">
                            </button>
                        </form>` : ""}
                    </div>
                </div>
            </div>
        </div>
    `;
    return col;
}

function mostrarError(error) {
    const contentContainer = document.getElementById("content-container");
    if (!contentContainer) {
        console.error("Error: No se encontró el elemento #content-container en el DOM.");
        return;
    }

    contentContainer.innerHTML = `<p style="color: red;">${error}</p>`;
}
