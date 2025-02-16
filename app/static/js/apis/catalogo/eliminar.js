document.addEventListener("DOMContentLoaded", () => {
    const modulo = obtenerModulo();
    const itemId = obtenerItemId();
    if (!modulo || !itemId) return;

    mostrarConfirmacionEliminar(modulo, itemId);
});

function obtenerModulo() {
    const pathSegments = window.location.pathname.split("/");
    return pathSegments[2] || null;
}

function obtenerItemId() {
    const pathSegments = window.location.pathname.split("/");
    return pathSegments[4] || null;
}

function mostrarConfirmacionEliminar(modulo, itemId) {
    const contentContainer = document.getElementById("content-container");
    contentContainer.innerHTML = "";

    // Crear el título y el mensaje de confirmación
    const titulo = document.createElement("h2");
    titulo.className = "display-4 text-primary text-center";
    titulo.textContent = `Eliminar ${modulo}`;

    const mensaje = document.createElement("p");
    mensaje.className = "lead text-muted text-center";
    mensaje.textContent = `¿Estás seguro de que deseas eliminar este ${modulo.toLowerCase()}?`;

    // Crear un contenedor para los botones
    const botonesContainer = document.createElement("div");
    botonesContainer.className = "d-flex justify-content-center mt-4";

    // Botón de cancelar
    const cancelarButton = document.createElement("a");
    cancelarButton.href = `/catalogo/${modulo}`;
    cancelarButton.className = "btn btn-secondary me-3";
    cancelarButton.textContent = "Cancelar";

    // Botón de eliminar
    const eliminarButton = document.createElement("button"); // Cambiado a <button>
    eliminarButton.className = "btn btn-danger";
    eliminarButton.textContent = "Eliminar";

    // Manejar el clic en el botón de eliminar
    eliminarButton.addEventListener("click", async (event) => {
        event.preventDefault(); // Detiene la acción por defecto
        try {
            const response = await eliminarContenido(modulo, itemId);
            if (response.ok) {
                window.location.href = `/catalogo/${modulo}`; // Redirigir al catálogo después de eliminar
            } else {
                const error = await response.json();
                mostrarError(error.error || "Error al eliminar el contenido.");
            }
        } catch (error) {
            mostrarError("Error en la solicitud.");
        }
    });

    // Agregar los botones al contenedor
    botonesContainer.appendChild(cancelarButton);
    botonesContainer.appendChild(eliminarButton);

    // Agregar el título, el mensaje y los botones al contenedor
    contentContainer.appendChild(titulo);
    contentContainer.appendChild(mensaje);
    contentContainer.appendChild(botonesContainer);
}

async function eliminarContenido(modulo, itemId) {
    return await fetch(`/catalogo/${modulo}/eliminar/${itemId}/`, {
        method: "POST",
        credentials: "include" // Asegura que se envíen cookies de sesión si es necesario
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
