document.addEventListener("DOMContentLoaded", async () => {
    await esperarCargaMenu();
    if (window.location.pathname === "/") {
        mostrarCarrusel();
    }

    window.addEventListener("popstate", () => {
        if (window.location.pathname === "/") {
            mostrarCarrusel();
        }
    });
});

async function esperarCargaMenu() {
    return new Promise((resolve) => {
        const observer = new MutationObserver(() => {
            const homeLink = document.querySelector(".home-link");
            if (homeLink) {
                observer.disconnect();
                resolve();
            }
        });

        observer.observe(document.body, { childList: true, subtree: true });
    });
}

function mostrarCarrusel() {
async function mostrarCarrusel() {
    const contentContainer = document.getElementById("content-container");

    if (!contentContainer) {
        console.error("Elemento content-container no encontrado.");
        return;
    }

    // Limpiar el contenido antes de insertar el carrusel
    contentContainer.innerHTML = "";

    // Crear y agregar el carrusel
    const carouselContainer = crearCarrusel();
    contentContainer.appendChild(carouselContainer);

    // Agregar evento al enlace de home solo una vez
    const homeLink = document.querySelector(".home-link");
    if (homeLink && !homeLink.dataset.eventAdded) {
        homeLink.addEventListener("click", async (e) => {
            e.preventDefault();
            window.history.pushState({}, '', '/');
            mostrarCarrusel();
        });
        homeLink.dataset.eventAdded = "true"; // Evitar múltiples eventos
    }
}

function crearCarrusel() {
    const carouselContainer = document.createElement("div");
    carouselContainer.className = "carousel-container";

    const carousel = document.createElement("div");
    carousel.id = "carouselExample";
    carousel.className = "carousel slide carousel-fade";
    carousel.setAttribute("data-bs-ride", "carousel");

    carousel.innerHTML = `
        <div class="carousel-indicators">
            <button type="button" data-bs-target="#carouselExample" data-bs-slide-to="0" class="active"></button>
            <button type="button" data-bs-target="#carouselExample" data-bs-slide-to="1"></button>
            <button type="button" data-bs-target="#carouselExample" data-bs-slide-to="2"></button>
        </div>

        <div class="carousel-inner">
            ${crearItemCarrusel("Materias", "/catalogo/Materias/", "/static/images/carrusel/materias1.jpg")}
            ${crearItemCarrusel("Juegos", "/catalogo/Juegos/", "/static/images/carrusel/juegos.jpg")}
            ${crearItemCarrusel("Proyectos", "/catalogo/Proyectos/", "/static/images/carrusel/proyectos.jpg")}
    const response = await fetch("/api/catalogo/carrusel/", {
        method: "GET",
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("token") // O cualquier método que uses para manejar tokens
        }
    });

    const data = await response.json();
    if (data.error) {
        contentContainer.innerHTML = `<p>${data.error}</p>`;  // Corregido para mostrar el error
        return;
    }

    const carouselHTML = `
        <div class="carousel-container">
            <div id="carouselExample" class="carousel slide carousel-fade" data-bs-ride="carousel">
                <div class="carousel-indicators">
                    ${data.carrusel.length > 1 ? `<button type="button" data-bs-target="#carouselExample" data-bs-slide-to="0" class="active"></button>` : ''}
                    ${data.carrusel.length > 1 ? `<button type="button" data-bs-target="#carouselExample" data-bs-slide-to="1"></button>` : ''}
                    ${data.carrusel.length > 2 ? `<button type="button" data-bs-target="#carouselExample" data-bs-slide-to="2"></button>` : ''}
                </div>
                <div class="carousel-inner">
                    ${data.carrusel.map((module, index) => `
                        <div class="carousel-item ${index === 0 ? 'active' : ''}">
                            <a href="/catalogo/${module.module}/" class="list-link" data-modulo="${module.module}">
                                <img src="${module.image}" class="d-block carousel-img" alt="${module.module}">
                            </a>
                        </div>
                    `).join('')}
                </div>
                <button class="carousel-control-prev" type="button" data-bs-target="#carouselExample" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Anterior</span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#carouselExample" data-bs-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Siguiente</span>
                </button>
            </div>
        </div>
    `;

    carouselContainer.appendChild(carousel);
    return carouselContainer;
}

function crearItemCarrusel(titulo, enlace, imagen) {
    return `
        <div class="carousel-item ${titulo === "Materias" ? "active" : ""}">
            <a href="${enlace}" class="list-link" data-modulo="${titulo}">
                <img src="${imagen}" class="d-block carousel-img" alt="${titulo}">
            </a>
        </div>
    `;
}

    contentContainer.innerHTML = carouselHTML;
}


// ✅ *CSS con diseño mejorado*
const style = document.createElement("style");
style.innerHTML = `
    .carousel-container {
    width: 60%;
    max-width: 900px;
    height: 400px;
    margin: auto;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 10px;
    padding: 5px;
    position: relative;
    background: linear-gradient(135deg, rgba(110, 142, 251, 0.5), rgba(167, 119, 227, 0.5));
    border: 3px solid transparent;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
    animation: glow 1.5s infinite alternate;
}

.carousel {
    width: 100%;
    height: 100%;
}

.carousel-inner {
    width: 100%;
    height: 100%;
}

.carousel-item {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.carousel-item a {
    width: 100%;
    height: 100%;
    display: flex;
}

.carousel-img {
    width: 100%;
    height: 100%;
    max-height: 100%;
    object-fit: cover;
    border-radius: 10px;
    transition: transform 0.3s ease-in-out;
}

.carousel-item a:hover .carousel-img {
    transform: scale(1.03);
}

@keyframes glow {
    0% {
        border-color: rgba(110, 142, 251, 0.8);
        box-shadow: 0px 0px 15px rgba(110, 142, 251, 0.3);
    }
    100% {
        border-color: rgba(167, 119, 227, 0.8);
        box-shadow: 0px 0px 20px rgba(167, 119, 227, 0.4);
    }
}

`;
document.head.appendChild(style);
