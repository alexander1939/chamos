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

async function mostrarCarrusel() {
    const contentContainer = document.getElementById("content-container");

    if (!contentContainer) {
        console.error("Elemento content-container no encontrado.");
        return;
    }

    // Limpiar el contenido antes de insertar el carrusel
    contentContainer.innerHTML = "";

    try {
        const response = await fetch("/api/catalogo/carrusel/", {
            method: "GET",
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("token") // O cualquier método que uses para manejar tokens
            }
        });

        const data = await response.json();
        if (data.error) {
            contentContainer.innerHTML = `<p>${data.error}</p>`;
            return;
        }

        const carouselContainer = crearCarrusel(data.carrusel);
        contentContainer.appendChild(carouselContainer);
    } catch (error) {
        console.error("Error al cargar el carrusel:", error);
        contentContainer.innerHTML = "<p>Error al cargar el carrusel.</p>";
    }

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

function crearCarrusel(items) {
    const carouselContainer = document.createElement("div");
    carouselContainer.className = "carousel-container";

    const carousel = document.createElement("div");
    carousel.id = "carouselExample";
    carousel.className = "carousel slide carousel-fade";
    carousel.setAttribute("data-bs-ride", "carousel");

    const indicators = items.map((_, index) => `
        <button type="button" data-bs-target="#carouselExample" data-bs-slide-to="${index}" ${index === 0 ? 'class="active"' : ''}></button>
    `).join('');

    const slides = items.map((item, index) => `
        <div class="carousel-item ${index === 0 ? 'active' : ''}">
            <a href="/catalogo/${item.module}/" class="list-link" data-modulo="${item.module}">
                <img src="${item.image}" class="d-block carousel-img" alt="${item.module}">
                <div class="carousel-caption-custom">${item.module}</div>
            </a>
        </div>
    `).join('');

    carousel.innerHTML = `
        <div class="carousel-indicators">
            ${indicators}
        </div>
        <div class="carousel-inner">
            ${slides}
        </div>
        <button class="carousel-control-prev" type="button" data-bs-target="#carouselExample" data-bs-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Anterior</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#carouselExample" data-bs-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Siguiente</span>
        </button>
    `;

    carouselContainer.appendChild(carousel);
    return carouselContainer;
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

    .carousel-caption-custom {
    position: absolute;
    bottom: 25px; /* Subir un poco el texto */
    left: 50%;
    transform: translateX(-50%);
    color: white;
    font-size: 18px;
    font-weight: bold;
    background: none; /* Quitar el fondo negro */
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); /* Agregar sombra para mejor visibilidad */
    opacity: 0;
    transition: opacity 0.3s ease-in-out;
    pointer-events: none;
}

.carousel-item:hover .carousel-caption-custom {
    opacity: 1;
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
