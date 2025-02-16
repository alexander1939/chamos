
document.addEventListener("DOMContentLoaded", () => {
    loadContent(window.location.pathname);

    // Maneja los clics en los enlaces de navegación para cargar contenido dinámico sin recargar la página.
    document.body.addEventListener("click", (e) => {
        const link = e.target.closest(".nav-link");
        if (link) {
            e.preventDefault();
            const url = link.getAttribute("href");
            loadContent(url);
            history.pushState(null, "", url);
        }
    });

    // Este evento se dispara cuando el usuario navega hacia atrás o adelante en el historial.
    window.addEventListener("popstate", () => {
        loadContent(window.location.pathname);
    });

    // Este evento se ejecuta antes de que el usuario abandone la página.
    window.addEventListener("beforeunload", () => {
        clearContent();
    });
});

/*
    La función loadContent carga contenido de forma dinámica a partir de la URL proporcionada.
    Hace una solicitud `fetch` a la URL y obtiene el contenido HTML de la página. Si la solicitud es exitosa, 
    se procesa el HTML recibido y se inyecta en la página actual. Si hay algún error, se maneja según el tipo de error.
    Además, se ejecutan los scripts dinámicos que forman parte del contenido cargado, asegurando que los scripts 
    de la nueva página se ejecuten correctamente.
*/
async function loadContent(url) {
    try {
        const response = await fetch(url, {
            method: "GET",
            credentials: "include",
            headers: {
                "Content-Type": "text/html",
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

        // Reemplaza el contenido del <main>
        document.querySelector("main").innerHTML = newDoc.querySelector("main").innerHTML;

        // Ejecuta los scripts dinámicos
        ejecutarScriptsDinamicos(newDoc);

        // Si la URL pertenece al catálogo, inicia el catálogo
        if (url.startsWith("/catalogo/")) {
            iniciarCatalogo();
        }

    } catch (error) {
        console.error("Error al cargar el contenido:", error);
    }
}


/*
    La función ejecutarScriptsDinamicos se encarga de ejecutar los scripts que forman parte del contenido HTML cargado.
    Recorre todos los elementos <script> dentro del nuevo contenido y los ejecuta dinámicamente. Si el script tiene un atributo `src`,
    se crea un nuevo <script> con el atributo `src` correspondiente. Si el script tiene contenido embebido, simplemente se ejecuta ese código.
    Esto asegura que los scripts de la nueva página se ejecuten correctamente.
*/
function ejecutarScriptsDinamicos(newDoc) {
    console.log("Ejecutando scripts de la nueva página...");

    newDoc.querySelectorAll("script").forEach((oldScript) => {
        const newScript = document.createElement("script");
        if (oldScript.src) {
            newScript.src = oldScript.src;
            newScript.async = true;
        } else {
            newScript.textContent = oldScript.textContent;
        }
        document.body.appendChild(newScript);
    });
}

/*
    La función clearContent se utiliza para limpiar el contenido del <main> cuando el usuario está a punto de abandonar la página.
    Esto asegura que el contenido se elimine antes de salir, evitando que la información quede en la página.
*/
function clearContent() {
    document.querySelector('main').innerHTML = '';
    console.log("Contenido eliminado al salir de la página.");
}
