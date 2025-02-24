// Espera a que el DOM esté completamente cargado antes de inicializar el buscador
// Esto garantiza que los elementos necesarios estén disponibles en el DOM
document.addEventListener("DOMContentLoaded", () => {
    inicializarBuscador();
});

// Variables globales para la paginación y control de búsqueda
let currentPage = 1; // Página actual en la paginación
const limit = 6; // Número de tarjetas por carga
let isLoading = false; // Flag para evitar múltiples llamadas simultáneas a la API
let queryActual = ""; // Última consulta de búsqueda ingresada por el usuario
let categoryActual = ""; // Última categoría seleccionada por el usuario
let hayMasResultados = true; // Controla si hay más resultados por cargar

/**
 * Inicializa el buscador.
 * - Obtiene los elementos del formulario de búsqueda y verifica su existencia.
 * - Asigna eventos para manejar la búsqueda de datos y la carga dinámica al hacer scroll.
 */
function inicializarBuscador() {
    const searchForm = document.getElementById("search-form-avanzado");
    const searchInput = document.getElementById("search-input-avanzado");
    const categorySelect = document.getElementById("category-select");
    const contentContainer = document.getElementById("content-container");

    // Verifica que los elementos del formulario existan en el DOM
    if (!searchForm || !searchInput || !categorySelect || !contentContainer) {
        console.error("Elementos del buscador no encontrados en el DOM.");
        return;
    }

    // Manejo del evento submit para iniciar la búsqueda
    searchForm.addEventListener("submit", async (e) => {
        e.preventDefault(); // Evita el envío por defecto del formulario
        queryActual = searchInput.value.trim();
        categoryActual = categorySelect.value;
    
        // Normalizar la categoría antes de enviarla a la API
        const categoryMap = {
            "Gestionar Privilegios": "privilegios",
            "Juegos": "juegos",
            "Materias": "materias",
            "Proyectos": "proyectos",
            "Todos": "todos"
        };
    
        categoryActual = categoryMap[categoryActual] || categoryActual.toLowerCase();
    
        if (queryActual) {
            if (!categoryActual || categoryActual === "") {
                mostrarMensaje("Por favor, selecciona una categoría válida.");
                return;
            }
    
            // Reinicia los parámetros de paginación y limpia los resultados previos
            currentPage = 1;
            hayMasResultados = true;
            contentContainer.innerHTML = "";
            await cargarResultados(); // Cargar los primeros resultados
        } else {
            mostrarMensaje("Por favor, ingresa un término de búsqueda.");
        }
    });
    

    // Evento de scroll para cargar más resultados dinámicamente
    window.addEventListener("scroll", async () => {
        // Verificar que haya una búsqueda activa antes de intentar cargar más resultados
        if (!queryActual || !categoryActual || isLoading || !hayMasResultados) return;
    
        const scrollPos = window.innerHeight + window.scrollY;
        const pageHeight = document.documentElement.scrollHeight;
    
        if (scrollPos >= pageHeight - 50) {
            currentPage++;
            await cargarResultados();
        }
    });
    
}

/**
 * Realiza una consulta a la API para obtener los resultados de la búsqueda.
 * Implementa la paginación solicitando un número limitado de resultados por página.
 */
async function cargarResultados() {
    if (isLoading || !hayMasResultados) return;
    isLoading = true; // Marca el estado de carga activa

    try {
        const url = `/api/search?query=${encodeURIComponent(queryActual)}&category=${encodeURIComponent(categoryActual)}&page=${currentPage}&limit=${limit}`;

        const response = await fetch(url, {
            method: "GET",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
        });

        if (!response.ok) {
            throw new Error(`Error en la búsqueda (Código ${response.status}): ${response.statusText}`);
        }

        const resultados = await response.json();

        if (resultados.length < limit) {
            hayMasResultados = false; // Si se recibieron menos resultados que el límite, no hay más para cargar
        }

        mostrarResultados(resultados, categoryActual);
    } catch (error) {
        console.error("Error al buscar en el backend:", error);
    } finally {
        isLoading = false; // Desactiva el estado de carga
    }
}

/**
 * Muestra los resultados en tarjetas dentro del contenedor de contenido.
 * Si se trata de una nueva búsqueda, limpia los resultados previos antes de agregar los nuevos.
 * Cada tarjeta contiene información sobre el resultado y un enlace para ver más detalles.
 */
function mostrarResultados(resultados, categoriaSeleccionada) {
    const contentContainer = document.getElementById("content-container");

    if (resultados.length === 0 && currentPage === 1) {
        contentContainer.innerHTML = "<p>No se encontraron resultados.</p>";
        return;
    }

    let cardsContainer = document.getElementById("cards-container");
    if (!cardsContainer) {
        cardsContainer = document.createElement("div");
        cardsContainer.id = "cards-container";
        cardsContainer.classList.add("row", "g-4");
        contentContainer.appendChild(cardsContainer);
    }

    resultados.forEach(item => {
        const col = document.createElement("div");
        col.classList.add("col-12", "col-sm-6", "col-md-4", "col-lg-4");

        const card = document.createElement("div");
        card.classList.add("card", "h-100", "shadow-sm", "clickable-card");

        if (categoriaSeleccionada === "privilegios") {
            // Renderizar usuarios
            card.innerHTML = `
                <div class="card-header">
                    <h5>${item.name} ${item.surnames}</h5>
                </div>
                <div class="card-body">
                    <p><strong>Correo:</strong> ${item.email}</p>
                    <p><strong>Teléfono:</strong> ${item.phone || "No disponible"}</p>
                    <p><strong>Privilegios:</strong></p>
                    <ul>
                        ${item.privileges.map(priv => `<li>${priv.name}</li>`).join("")}
                    </ul>
                </div>
            `;

            // Redirigir al usuario al hacer clic en la tarjeta
            // card.addEventListener("click", () => {
            //     window.location.href = `/catalogo/detalle/${item.id}/`;
            // });

        } else {
            // Renderizar módulos
            const categoriaInfo = categoriaSeleccionada === "todos"
                ? `<p class="card-category"><strong>Categoría:</strong> ${item.categoria}</p>`
                : "";

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
        }

        col.appendChild(card);
        cardsContainer.appendChild(col);
    });
}


/**
 * Muestra un mensaje en el contenedor de contenido.
 * Se usa para indicar errores o mensajes informativos cuando no hay resultados.
 */
function mostrarMensaje(mensaje) {
    const contentContainer = document.getElementById("content-container");
    contentContainer.innerHTML = `<p>${mensaje}</p>`;
}
