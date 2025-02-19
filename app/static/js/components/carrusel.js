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

function mostrarCarrusel() {
    const contentContainer = document.getElementById("content-container");
    if (!contentContainer) return;

    contentContainer.innerHTML = ""; // Limpiar el contenido antes de insertar el carrusel

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
            <div class="carousel-item active">
                <a href="/catalogo/Materias/" class="list-link" data-modulo="Materias">
                    <img src="/static/images/carrusel/materias1.jpg" class="d-block carousel-img" alt="Materias">
                </a>
            </div>
            <div class="carousel-item">
                <a href="/catalogo/Juegos/" class="list-link" data-modulo="Juegos">
                    <img src="/static/images/carrusel/juegos.jpg" class="d-block carousel-img" alt="Juegos">
                </a>
            </div>
            <div class="carousel-item">
                <a href="/catalogo/Proyectos/" class="list-link" data-modulo="Proyectos">
                    <img src="/static/images/carrusel/proyectos.jpg" class="d-block carousel-img" alt="Proyectos">
                </a>
            </div>
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
    contentContainer.appendChild(carouselContainer);
}

// ✅ **CSS con diseño mejorado**
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
