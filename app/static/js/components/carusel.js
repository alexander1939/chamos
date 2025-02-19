document.addEventListener("DOMContentLoaded", async () => {
    if (window.location.pathname === "/") {
        mostrarCarrusel("Galería"); // Muestra el carrusel en la raíz
    }

    inicializarUsuarios();

    window.addEventListener("popstate", () => {
        if (window.location.pathname === "/") {
            mostrarCarrusel("Galería");
        }
    });
});

function mostrarCarrusel(modulo) {
    const contentContainer = document.getElementById("content-container");
    if (!contentContainer) return;

    contentContainer.innerHTML = "";

    const titulo = document.createElement("h2");
    titulo.className = "display-4 text-primary text-center";
    titulo.textContent = `Galería de ${modulo}`;

    const descripcion = document.createElement("p");
    descripcion.className = "lead text-muted text-center";
    descripcion.textContent = `Explora las imágenes de ${modulo.toLowerCase()}.`;

    // Carrusel de Bootstrap
    const carousel = document.createElement("div");
    carousel.id = "carouselExample";
    carousel.className = "carousel slide";
    carousel.setAttribute("data-bs-ride", "carousel");

    carousel.innerHTML = `
    <div class="carousel-inner">
        <div class="carousel-item active">
            <a href="/catalogo/Materias/">
                <img src="https://i.pinimg.com/736x/03/8c/0a/038c0a700b714ba6514b1e4acfdc9b62.jpg" class="d-block w-100" alt="Imagen 1">
            </a>
        </div>
        <div class="carousel-item">
            <a href="/catalogo/Juegos/">
                <img src="https://flowgpt.com/_next/image?url=https%3A%2F%2Fimage-cdn.flowgpt.com%2Fprompt%2FDBucU6uoe9KBnXkwDRLmx%2F1694840467243&w=1920&q=75" class="d-block w-100" alt="Imagen 2">
            </a>
        </div>
        <div class="carousel-item">
            <a href="/catalogo/Proyectos/">
                <img src="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/43ed4d38-6d57-4862-88d8-f3b46e7b4397/dckcyft-8582c814-c860-4d6f-80f5-0d06c46ddbdf.jpg/v1/fill/w_1024,h_751,q_75,strp/goku_black_redo_by_midgetman352_dckcyft-fullview.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9NzUxIiwicGF0aCI6IlwvZlwvNDNlZDRkMzgtNmQ1Ny00ODYyLTg4ZDgtZjNiNDZlN2I0Mzk3XC9kY2tjeWZ0LTg1ODJjODE0LWM4NjAtNGQ2Zi04MGY1LTBkMDZjNDZkZGJkZi5qcGciLCJ3aWR0aCI6Ijw9MTAyNCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.cfptxf7nKEhWwHw8IEIQhdAATrigg87DfKV3_B6zgl4" class="d-block w-100" alt="Imagen 3">
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


    contentContainer.appendChild(titulo);
    contentContainer.appendChild(descripcion);
    contentContainer.appendChild(carousel);
}
