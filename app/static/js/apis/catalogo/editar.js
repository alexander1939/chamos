document.addEventListener("DOMContentLoaded", async () => {
    console.log("Página cargada, verificando el módulo y el ID...");
    
    const modulo = obtenerModulo();
    const itemId = obtenerItemId();
    
    if (!modulo || !itemId) {
        console.error("Módulo o ID no detectados.");
        mostrarError("Error al detectar el módulo o ID.");
        return;
    }

    try {
        const data = await obtenerDetalleParaEditar(modulo, itemId);
        mostrarFormularioEditar(data, modulo, itemId);
    } catch (error) {
        mostrarError("No se pudo obtener los detalles para la edición.");
    }
});

function obtenerModulo() {
    const pathSegments = window.location.pathname.split("/");
    return pathSegments[2] || null;
}

function obtenerItemId() {
    const pathSegments = window.location.pathname.split("/");
    return pathSegments[4] || null;
}

async function obtenerDetalleParaEditar(modulo, itemId) {
    try {
        const response = await fetch(`/api/catalogo/detalle/?modulo=${modulo}&id=${itemId}`, {
            method: "GET",
            credentials: "include",
            headers: { "Accept": "application/json" }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Error ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error("Error obteniendo detalle:", error);
        throw error;
    }
}



function mostrarFormularioEditar(data, modulo, itemId) {
    console.log("Datos recibidos para edición:", data);

    if (!data || data.error) {
        mostrarError(data.error || "No se encontró información del detalle.");
        return;
    }

    const detalle = data.detalle;
    const contentContainer = document.getElementById("content-container");

    if (!contentContainer) {
        console.error("Error: No se encontró el elemento #content-container en el DOM.");
        return;
    }

    contentContainer.innerHTML = `
        <h2 class="display-4 text-primary text-center">Editar ${modulo}</h2>
        <form id="form-editar" class="mt-4">
            <div class="form-group">
                <label for="nombre">Nombre</label>
                <input type="text" class="form-control" id="nombre" name="nombre" value="${detalle.nombre}" required>
            </div>
            <div class="form-group">
                <label for="descripcion">Descripción</label>
                <textarea class="form-control" id="descripcion" name="descripcion" rows="3" required>${detalle.descripcion}</textarea>
            </div>
            <button type="submit" class="btn btn-primary">Guardar cambios</button>
            <div id="loading" style="display: none; color: green;">Guardando cambios...</div>
        </form>
    `;

    document.getElementById("form-editar").addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const nombre = document.getElementById("nombre").value.trim();
        const descripcion = document.getElementById("descripcion").value.trim();

        if (!nombre || !descripcion) {
            mostrarError("Debe proporcionar nombre y descripción.");
            return;
        }

        document.getElementById("loading").style.display = "block";

        try {
            await editarContenido(modulo, itemId, nombre, descripcion);
            alert("Edición exitosa");
            window.location.href = `/catalogo/${modulo}`;
        } catch (error) {
            mostrarError("Error al editar el contenido.");
        } finally {
            document.getElementById("loading").style.display = "none";
        }
    });
}

async function editarContenido(modulo, itemId, nombre, descripcion) {
    try {
        const response = await fetch(`/api/catalogo/editar/?modulo=${modulo}`, {
            method: "PUT",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id: itemId, nombre, descripcion })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Error al editar el contenido.");
        }
    } catch (error) {
        console.error("Error editando contenido:", error);
        throw error;
    }
}

function mostrarError(error) {
    const contentContainer = document.getElementById("content-container");
    if (!contentContainer) return;

    let errorMessage = document.getElementById("error-message");
    if (!errorMessage) {
        errorMessage = document.createElement("p");
        errorMessage.id = "error-message";
        errorMessage.style.color = "red";
        contentContainer.appendChild(errorMessage);
    }

    errorMessage.textContent = error;
}
