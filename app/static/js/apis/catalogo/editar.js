document.addEventListener("DOMContentLoaded", async () => {
    inicializarEditar();
    actualizarBreadcrumbs();

    const modulo = obtenerModulo();
    const itemId = obtenerItemId();
    const esEdicion = window.location.pathname.includes("editar");

    if (modulo && itemId && esEdicion) {
        try {
            const data = await obtenerDetalleParaEditar(modulo, itemId);
            mostrarFormularioEditar(data, modulo, itemId);
            actualizarBreadcrumbs();
        } catch (error) {
            Swal.fire("Error", "No se pudo obtener los detalles para la edición.", "error");
        }
    }
});

function inicializarEditar() {
    document.body.addEventListener("click", async (e) => {
        const botonEditar = e.target.closest(".btn-editar");
        if (botonEditar) {
            e.preventDefault();
            const modulo = botonEditar.getAttribute("data-modulo");
            const itemId = botonEditar.getAttribute("data-id");

            if (modulo && itemId) {
                history.pushState({}, '', `/catalogo/${modulo}/editar/${itemId}/`);
                await cargarFormularioEditar(modulo, itemId);
            }
        }
    });
}

async function cargarFormularioEditar(modulo, itemId) {
    const contentContainer = document.getElementById("content-container");
    if (!contentContainer) return;

    try {
        contentContainer.innerHTML = `<p>Cargando formulario de edición...</p>`;

        const response = await fetch(`/api/catalogo/detalle/?modulo=${modulo}&id=${itemId}`, {
            method: "GET",
            credentials: "include",
            headers: { "Accept": "application/json" }
        });

        if (!response.ok) {
            throw new Error("Error al obtener los detalles del ítem.");
        }

        const data = await response.json();
        const item = data.detalle;

        if (!item) {
            contentContainer.innerHTML = `<p style="color: red;">Error: No se encontraron los detalles.</p>`;
            return;
        }

        contentContainer.innerHTML = `
            <h2 class="display-4 text-primary text-center">Editar ${modulo}</h2>
            <form id="form-editar" class="mt-4">
                <div class="form-group">
                    <label for="nombre">Nombre</label>
                    <input type="text" class="form-control" id="nombre" name="nombre" value="${item.nombre}" required>
                </div>
                <div class="form-group">
                    <label for="descripcion">Descripción</label>
                    <textarea class="form-control" id="descripcion" name="descripcion" rows="3" required>${item.descripcion}</textarea>
                </div>
                <button type="submit" class="btn btn-primary">Guardar cambios</button>
                <div id="loading" style="display: none; color: green;">Guardando cambios...</div>
            </form>
        `;

        document.getElementById("form-editar").addEventListener("submit", async (e) => {
            e.preventDefault();
            await enviarEdicion(modulo, itemId);
        });

        actualizarBreadcrumbs();

    } catch (error) {
        contentContainer.innerHTML = `<p style="color: red;">Error al cargar el formulario.</p>`;
        console.error("Error al obtener los detalles del ítem:", error);
    }
}

async function enviarEdicion(modulo, itemId) {
    const nombre = document.getElementById("nombre").value.trim();
    const descripcion = document.getElementById("descripcion").value.trim();

    if (!nombre || !descripcion) {
        Swal.fire("Error", "Debe proporcionar nombre y descripción.", "error");
        return;
    }

    try {
        const response = await fetch(`/api/catalogo/editar/?modulo=${modulo}`, {
            method: "PUT",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id: itemId, nombre, descripcion })
        });

        if (!response.ok) {
            throw new Error("Error al editar el contenido.");
        }

        Swal.fire({
            icon: "success",
            title: "¡Éxito!",
            text: "El contenido se ha editado correctamente.",
            confirmButtonText: "Aceptar"
        }).then(() => {
            history.pushState({}, '', `/catalogo/${modulo}/`);
            cargarCatalogo(modulo); // 🔄 Actualizar solo el main sin recargar la página
        });

    } catch (error) {
        console.error("Error editando contenido:", error);
        Swal.fire("Error", "No se pudo editar el contenido.", "error");
    }
}
