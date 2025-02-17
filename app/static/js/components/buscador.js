// buscador.js

document.addEventListener("DOMContentLoaded", () => {
    inicializarBuscador();
});

function inicializarBuscador() {
    const searchForm = document.getElementById("search-form-avanzado");
    const searchInput = document.getElementById("search-input-avanzado");
    const categorySelect = document.getElementById("category-select");
    const contentContainer = document.getElementById("content-container");

    if (!searchForm || !searchInput || !categorySelect || !contentContainer) {
        console.error("Elementos del buscador no encontrados en el DOM.");
        return;
    }

    searchForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const query = searchInput.value.trim();
        const category = categorySelect.value;

        if (query) {
            if (!category || category === "") {
                mostrarMensaje("Por favor, selecciona una categoría válida.");
                return;
            }

            const resultados = await buscarEnBackend(query, category);
            if (resultados.error) {
                mostrarMensaje(resultados.error);
            } else {
                mostrarResultados(resultados, category);
            }
        } else {
            mostrarMensaje("Por favor, ingresa un término de búsqueda.");
        }
    });
}


async function buscarEnBackend(query, category) {
    try {
        const categoryLower = category.toLowerCase();
        const url = `/api/search?query=${encodeURIComponent(query)}&category=${encodeURIComponent(categoryLower)}`;

        const response = await fetch(url, {
            method: "GET",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
        });

        if (!response.ok) {
            throw new Error(`Error en la búsqueda (Código ${response.status}): ${response.statusText}`);
        }

        const resultados = await response.json();
        return resultados;
    } catch (error) {
        console.error("Error al buscar en el backend:", error);
        return { error: "Error al conectar con el servidor." };
    }
}

function mostrarResultados(resultados, categoriaSeleccionada) {
    const contentContainer = document.getElementById("content-container");

    if (resultados.length === 0) {
        contentContainer.innerHTML = "<p>No se encontraron resultados.</p>";
        return;
    }

    const cardsContainer = document.createElement("div");
    cardsContainer.id = "cards-container";
    cardsContainer.classList.add("row", "g-4");

    resultados.forEach(item => {
        const categoriaInfo = categoriaSeleccionada === "todos"
            ? `<p class="card-category"><strong>Categoría:</strong> ${item.categoria}</p>`
            : "";

        const col = document.createElement("div");
        col.classList.add("col-12", "col-sm-6", "col-md-5", "col-lg-3");

        const card = document.createElement("div");
        card.classList.add("card", "h-100", "shadow-sm");

        card.innerHTML = `
            <div class="card-body">
                <h5 class="card-title">${item.nombre}</h5>
                <p class="card-text">${item.descripcion}</p>
                ${categoriaInfo}
            </div>
            <div class="card-footer text-center">
            <a href="/catalogo/${item.categoria}/detalle/${item.id}/" class="deta-link btn btn-primary">Ver Detalles</a>
            </div>
        `;

        col.appendChild(card);
        cardsContainer.appendChild(col);
    });

    contentContainer.innerHTML = "";
    contentContainer.appendChild(cardsContainer);
}


function mostrarMensaje(mensaje) {
    const contentContainer = document.getElementById("content-container");
    contentContainer.innerHTML = `<p>${mensaje}</p>`;
}