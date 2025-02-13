document.addEventListener("DOMContentLoaded", () => {
    loadContent(window.location.pathname);

    document.body.addEventListener("click", (e) => {
        const link = e.target.closest(".nav-link");
        if (link) {
            e.preventDefault();
            const url = link.getAttribute("href");
            loadContent(url);
            history.pushState(null, "", url);
        }
    });

    window.addEventListener("popstate", () => {
        loadContent(window.location.pathname);
    });

    // Eliminar el contenido cuando el usuario abandone la página
    window.addEventListener("beforeunload", () => {
        clearContent();
    });
});

async function loadContent(url) {
    try {
        const response = await fetch(url, {
            method: "GET",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (!response.ok) {
            if (response.status === 401) {
                console.warn("Sesión expirada o token inválido. Redirigiendo a login...");
                window.location.href = "/login";
            } else {
                console.error(`Error en la API (Código ${response.status}): ${response.statusText}`);
            }
            return;
        }

        const html = await response.text();
        const newDoc = new DOMParser().parseFromString(html, "text/html");

        // Reemplaza solo el contenido del <main>
        document.querySelector('main').innerHTML = newDoc.querySelector('main').innerHTML;

        // Actualizar el menú si es necesario
        if (url !== window.location.pathname) {
            cargarDatos();  // Recarga el menú dinámico
        }

    } catch (error) {
        console.error("Error al cargar el contenido:", error);
    }
}

// Función para eliminar el contenido cargado
function clearContent() {
    document.querySelector('main').innerHTML = ''; // Elimina el contenido dentro de <main>
    console.log("Contenido eliminado al salir de la página.");
}
