document.addEventListener("DOMContentLoaded", () => {
    const modulo = obtenerModulo();
    if (!modulo) return;

    obtenerDatos(modulo)
        .then(data => mostrarDatos(data, modulo))
        .catch(error => mostrarError(error));
});

function obtenerModulo() {
    const pathSegments = window.location.pathname.split("/");
    return pathSegments[2] || null;
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
    contentContainer.innerHTML = "";

    if (data.error) {
        mostrarError(data.error);
        return;
    }

    const items = data.materias || data.proyectos || data.juegos || [];
    if (items.length === 0) {
        contentContainer.innerHTML = `<div class="alert alert-info">No hay registros disponibles.</div>`;
        return;
    }

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
    document.getElementById("content-container").innerHTML = `<p style="color: red;">${error}</p>`;
}
