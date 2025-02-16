// buscador.js

// Espera a que el DOM esté completamente cargado.
document.addEventListener("DOMContentLoaded", () => {
    inicializarBuscador();
});

function inicializarBuscador() {
    // Elementos del DOM.
    const searchForm = document.getElementById("search-form-avanzado");
    const searchInput = document.getElementById("search-input-avanzado");
    const categorySelect = document.getElementById("category-select"); // Selecciona el <select>.
    const contentContainer = document.getElementById("content-container");

    // Verifica que los elementos existan en el DOM.
    if (!searchForm || !searchInput || !categorySelect || !contentContainer) {
        console.error("Elementos del buscador no encontrados en el DOM.");
        return;
    }

    // Evento para manejar el envío del formulario de búsqueda.
    searchForm.addEventListener("submit", async (e) => {
        e.preventDefault(); // Evita que el formulario recargue la página.
        const query = searchInput.value.trim();
        const category = categorySelect.value; // Obtiene la categoría seleccionada.
    
        if (query) {
            // Valida la categoría antes de realizar la búsqueda.
            if (!category || category === "") {
                mostrarMensaje("Por favor, selecciona una categoría válida.");
                return;
            }
    
            // Realiza la búsqueda si hay un término válido.
            const resultados = await buscarEnBackend(query, category);
            if (resultados.error) {
                // Maneja el error del backend.
                mostrarMensaje(resultados.error);
            } else {
                mostrarResultados(resultados, category); // Pasa la categoría seleccionada.
            }
        } else {
            // Si no hay término de búsqueda, muestra un mensaje.
            mostrarMensaje("Por favor, ingresa un término de búsqueda.");
        }
    });
}


// Función para realizar la búsqueda en el backend.
async function buscarEnBackend(query, category) {
    try {
        const categoryLower = category.toLowerCase();
        // Construye la URL de búsqueda.
        const url = `/api/search?query=${encodeURIComponent(query)}&category=${encodeURIComponent(categoryLower)}`;

        // Realiza la solicitud al backend.
        const response = await fetch(url, {
            method: "GET",
            headers: { "Content-Type": "application/json" },
            credentials: "include", // Incluye las cookies (necesario para el token).
        });

        if (!response.ok) {
            throw new Error(`Error en la búsqueda (Código ${response.status}): ${response.statusText}`);
        }

        // Parsea la respuesta como JSON.
        const resultados = await response.json();
        return resultados;
    } catch (error) {
        console.error("Error al buscar en el backend:", error);
        return { error: "Error al conectar con el servidor." }; // Retorna un objeto de error.
    }
}

// Función para mostrar los resultados de la búsqueda en el DOM.
function mostrarResultados(resultados, categoriaSeleccionada) {
    const contentContainer = document.getElementById("content-container");

    if (resultados.length === 0) {
        contentContainer.innerHTML = "<p>No se encontraron resultados.</p>";
        return;
    }

    // Usar clases de Bootstrap para la cuadrícula responsiva.
    const cardsContainer = document.createElement("div");
    cardsContainer.id = "cards-container";
    cardsContainer.classList.add("row", "g-4"); // "g-4" para separación entre tarjetas.

    // Generar el HTML para las tarjetas.
    resultados.forEach(item => {
        const categoriaInfo = categoriaSeleccionada === "todos" 
            ? `<p class="card-category"><strong>Categoría:</strong> ${item.categoria}</p>` 
            : "";

        const col = document.createElement("div");
        col.classList.add("col-12", "col-sm-6", "col-md-5", "col-lg-3"); // Ajuste automático en diferentes tamaños.

        const card = document.createElement("div");
        card.classList.add("card", "h-100", "shadow-sm");

        card.innerHTML = `
            <div class="card-body">
                <h5 class="card-title">${item.nombre}</h5>
                <p class="card-text">${item.descripcion}</p>
                ${categoriaInfo}
            </div>
            <div class="card-footer text-center">
                <a href="${item.detalles_url}" class="btn btn-primary">Ver Detalles</a>
            </div>
        `;

        col.appendChild(card);
        cardsContainer.appendChild(col);
    });

    // Limpiar el contenedor principal y añadir el contenedor de tarjetas.
    contentContainer.innerHTML = "";
    contentContainer.appendChild(cardsContainer);
}


// Función para mostrar mensajes en el contenedor.
function mostrarMensaje(mensaje) {
    const contentContainer = document.getElementById("content-container");
    contentContainer.innerHTML = `<p>${mensaje}</p>`;
}