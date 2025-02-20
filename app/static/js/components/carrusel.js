document.addEventListener("DOMContentLoaded", async () => {
    if (window.location.pathname === "/") {
        mostrarCarrusel();
    }

    inicializarUsuarios();

    window.addEventListener("popstate", () => {
        if (window.location.pathname === "/") {
            mostrarCarrusel();
        }
    });
});

async function mostrarCarrusel() {
    const contentContainer = document.getElementById("content-container");
    if (!contentContainer) return;

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

    contentContainer.innerHTML = carouselHTML;
}


// ✅ *CSS con diseño mejorado*
const style = document.createElement("style");
style.innerHTML = `
    .carousel-container {
        width: 80%;
        max-width: 1200px; /* Máximo tamaño */
        height: 600px; /* Altura adaptable */
        margin: auto;
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 20px;
        padding: 10px;
        position: relative;
        background: linear-gradient(135deg, rgba(110, 142, 251, 0.5), rgba(167, 119, 227, 0.5));
        border: 4px solid transparent;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
        animation: glow 1.5s infinite alternate;
    }

    /* Efecto de borde brillante */
    @keyframes glow {
        0% {
            border-color: rgba(110, 142, 251, 0.8);
            box-shadow: 0px 0px 20px rgba(110, 142, 251, 0.4);
        }
        100% {
            border-color: rgba(167, 119, 227, 0.8);
            box-shadow: 0px 0px 25px rgba(167, 119, 227, 0.5);
        }
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
        object-fit: cover; /* Ajusta sin distorsionar */
        border-radius: 15px;
        transition: transform 0.3s ease-in-out;
    }

    /* Efecto de zoom al pasar el mouse sobre la imagen */
    .carousel-item a:hover .carousel-img {
        transform: scale(1.05);
    }
`;
document.head.appendChild(style);
