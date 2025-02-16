document.addEventListener("DOMContentLoaded", () => {
    const modulo = obtenerModulo();
    const itemId = obtenerItemId();
    if (!modulo || !itemId) return;

    obtenerDetalleParaEditar(modulo, itemId)
        .then(data => mostrarFormularioEditar(data, modulo, itemId))
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

async function obtenerDetalleParaEditar(modulo, itemId) {
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

function mostrarFormularioEditar(data, modulo, itemId) {
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
    titulo.textContent = `Editar ${modulo}`;

    const descripcion = document.createElement("p");
    descripcion.className = "lead text-muted text-center";
    descripcion.textContent = `Aquí puedes editar el ${modulo.toLowerCase()}.`;

    // Crear el formulario
    const form = document.createElement("form");
    form.id = "form-editar";
    form.className = "mt-4";

    // Campo para el nombre
    const nombreGroup = document.createElement("div");
    nombreGroup.className = "form-group";
    nombreGroup.innerHTML = `
        <label for="nombre">Nombre</label>
        <input type="text" class="form-control" id="nombre" name="nombre" value="${detalle.nombre}" required>
    `;

    // Campo para la descripción
    const descripcionGroup = document.createElement("div");
    descripcionGroup.className = "form-group";
    descripcionGroup.innerHTML = `
        <label for="descripcion">Descripción</label>
        <textarea class="form-control" id="descripcion" name="descripcion" rows="3" required>${detalle.descripcion}</textarea>
    `;

    // Botón de enviar
    const submitButton = document.createElement("button");
    submitButton.type = "submit";
    submitButton.className = "btn btn-primary";
    submitButton.textContent = `Editar ${modulo}`;

    // Agregar elementos al formulario
    form.appendChild(nombreGroup);
    form.appendChild(descripcionGroup);
    form.appendChild(submitButton);

    // Agregar el título, la descripción y el formulario al contenedor
    contentContainer.appendChild(titulo);
    contentContainer.appendChild(descripcion);
    contentContainer.appendChild(form);

    // Manejar el envío del formulario
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const nombre = document.getElementById("nombre").value;
        const descripcion = document.getElementById("descripcion").value;

        if (!nombre || !descripcion) {
            mostrarError("Debe proporcionar nombre y descripción.");
            return;
        }

        try {
            const response = await editarContenido(modulo, itemId, nombre, descripcion);
            if (response.ok) {
                window.location.href = `/catalogo/${modulo}`; // Redirigir al catálogo después de editar
            } else {
                const error = await response.json();
                mostrarError(error.error || "Error al editar el contenido.");
            }
        } catch (error) {
            mostrarError("Error en la solicitud.");
        }
    });
}

async function editarContenido(modulo, itemId, nombre, descripcion) {
    const data = { id: itemId, nombre, descripcion };
    return await fetch(`/api/catalogo/editar/?modulo=${modulo}`, {
        method: "PUT",
        credentials: "include", // Para enviar cookies si es necesario
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });
}

function mostrarError(error) {
    const contentContainer = document.getElementById("content-container");
    if (!contentContainer) {
        console.error("Error: No se encontró el elemento #content-container en el DOM.");
        return;
    }

    const errorMessage = document.createElement("p");
    errorMessage.style.color = "red";
    errorMessage.textContent = error;

    contentContainer.appendChild(errorMessage);
}