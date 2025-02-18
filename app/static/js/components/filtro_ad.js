document.addEventListener("DOMContentLoaded", () => {
    filtroBusqueda();
});

function filtroBusqueda() {
    const filtroContainer = document.getElementById("search-container");
    if (!filtroContainer) return;

    const filtroInput = document.getElementById("search-input");
    const filtroButton = document.getElementById("search-button");
    const filtroCancelButton = document.getElementById("cancel-search");

    if (!filtroInput || !filtroButton || !filtroCancelButton) return;

    filtroInput.addEventListener("input", () => {
        filtroCancelButton.style.display = filtroInput.value.trim() ? "inline-block" : "none";
    });

    filtroInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
            ejecutarFiltroBusqueda(filtroInput.value);
        }
    });

    filtroButton.addEventListener("click", () => {
        ejecutarFiltroBusqueda(filtroInput.value);
    });

    filtroCancelButton.addEventListener("click", async () => {
        filtroInput.value = "";
        filtroCancelButton.style.display = "none";
        await cargarCatalogo(obtenerModulo());
    });
}


async function ejecutarFiltroBusqueda(query, page = 1, limit = 6) {
    const moduloActual = obtenerModulo();
    const filtroContent = document.getElementById("content-container");

    if (!query.trim()) {
        mostrarMensajeError("Por favor ingresa un término para buscar.");
        return;
    }

    if (!moduloActual || !filtroContent) return;

    try {
        filtroContent.innerHTML = `<p>Buscando en ${moduloActual}...</p>`;

        const response = await fetch(`/api/search?query=${query}&category=${moduloActual}&page=${page}&limit=${limit}`, {
            method: "GET",
            credentials: "include",
            headers: { "Content-Type": "application/json" }
        });

        if (!response.ok) {
            throw new Error(`Error en la API: ${response.statusText}`);
        }

        const results = await response.json();
        mostrarDatos(results, moduloActual, true);

        const filtroCancelButton = document.getElementById("cancel-search");
        if (filtroCancelButton) {
            filtroCancelButton.style.display = query.trim() ? "inline-block" : "none";
        }

    } catch (error) {
        console.error("Error al buscar:", error);
        filtroContent.innerHTML = `<p style="color: red;">Error al realizar la búsqueda.</p>`;
    }
}

function mostrarMensajeError(message) {
    const contentContainer = document.getElementById("content-container");

    const alertMessage = document.createElement("div");
    alertMessage.className = "alert alert-warning alert-dismissible fade show";
    alertMessage.role = "alert";
    alertMessage.innerHTML = `
        <strong>Advertencia:</strong> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    contentContainer.prepend(alertMessage);

    setTimeout(() => {
        alertMessage.remove();
    }, 5000);
}
