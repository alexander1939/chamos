document.addEventListener("DOMContentLoaded", () => {
    // Cargar el contenido inicial
    loadContent(window.location.pathname);

    // Delegar eventos para manejar clics en enlaces del menú lateral
    document.body.addEventListener("click", (e) => {
        const link = e.target.closest(".nav-link");
        if (link) {
            e.preventDefault();
            const url = link.getAttribute("href");
            loadContent(url);
            history.pushState(null, "", url);
        }
    });

    // Manejar el evento de retroceso/avance del navegador
    window.addEventListener("popstate", () => {
        loadContent(window.location.pathname);
    });
});

async function loadContent(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error("Error al cargar la página");

        const text = await response.text();

        // Extraer solo el contenido del <main>
        const parser = new DOMParser();
        const doc = parser.parseFromString(text, "text/html");
        const newContent = doc.querySelector("#main").innerHTML;

        // Actualizar el contenido del <main>
        document.querySelector("#main").innerHTML = newContent;
    } catch (error) {
        console.error("Error:", error);
        document.querySelector("#main").innerHTML = "<p>Error al cargar la página.</p>";
    }
}
