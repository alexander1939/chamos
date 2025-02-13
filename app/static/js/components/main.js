/*
    Este bloque de código espera que el contenido del DOM se cargue completamente antes de ejecutar cualquier acción.
    Una vez que el DOM se ha cargado, se ejecutan varias funciones que permiten cargar contenido dinámicamente, 
    manejar la navegación y limpiar el contenido al salir de la página.
    Primero, se carga el contenido de la página utilizando la URL actual. Luego, se agrega un evento de clic en el cuerpo del documento
    para manejar la navegación por enlace sin recargar la página, usando el método `pushState` para modificar el historial del navegador.
    También se manejan los eventos del navegador para asegurarse de que el contenido se actualice correctamente al navegar hacia atrás o adelante.
    Finalmente, se agrega un evento `beforeunload` para limpiar el contenido cuando el usuario esté a punto de abandonar la página.
*/
document.addEventListener("DOMContentLoaded", () => {
    loadContent(window.location.pathname); // Carga el contenido inicial según la URL.

    // Maneja los clics en los enlaces de navegación para cargar contenido dinámico sin recargar la página.
    document.body.addEventListener("click", (e) => {
        const link = e.target.closest(".nav-link"); // Encuentra el enlace de navegación clicado.
        if (link) {
            e.preventDefault(); // Previne el comportamiento por defecto (recargar la página).
            const url = link.getAttribute("href"); // Obtiene la URL del enlace.
            loadContent(url); // Carga el contenido dinámicamente con la URL.
            history.pushState(null, "", url); // Modifica la URL en el navegador sin recargar la página.
        }
    });

    // Este evento se dispara cuando el usuario navega hacia atrás o adelante en el historial.
    window.addEventListener("popstate", () => {
        loadContent(window.location.pathname); // Carga el contenido correspondiente a la URL actual.
    });

    // Este evento se ejecuta antes de que el usuario abandone la página.
    window.addEventListener("beforeunload", () => {
        clearContent(); // Limpia el contenido del DOM cuando el usuario salga de la página.
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
        // Realiza una solicitud GET a la URL y obtiene el contenido HTML de la página.
        const response = await fetch(url, {
            method: "GET",
            credentials: "include",
            headers: {
                "Content-Type": "text/html", // Especifica que esperamos contenido HTML.
            },
        });

        // Si la respuesta no es exitosa (código de estado no es 2xx), maneja el error.
        if (!response.ok) {
            if (response.status === 401) {
                // Si la sesión ha expirado o el token es inválido, redirige al login.
                console.warn("Sesión expirada o token inválido. Redirigiendo a login...");
                window.location.href = "/login";
            } else {
                // Si ocurre otro error, muestra un mensaje de error con el código de estado.
                console.error(`Error en la API (Código ${response.status}): ${response.statusText}`);
            }
            return;
        }

        // Si la respuesta es exitosa, procesa el contenido HTML de la página.
        const html = await response.text();
        const newDoc = new DOMParser().parseFromString(html, "text/html"); // Parsea el contenido HTML recibido.

        // Actualiza el contenido del <main> con el nuevo contenido de la página.
        document.querySelector("main").innerHTML = newDoc.querySelector("main").innerHTML;

        // Ejecuta los scripts dinámicos que se incluyen en la nueva página cargada.
        ejecutarScriptsDinamicos(newDoc);

    } catch (error) {
        // Si ocurre algún error durante la solicitud o el procesamiento, se muestra un mensaje de error en la consola.
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

    // Recorre todos los scripts del nuevo documento y los ejecuta dinámicamente.
    newDoc.querySelectorAll("script").forEach((oldScript) => {
        const newScript = document.createElement("script");
        if (oldScript.src) {
            newScript.src = oldScript.src; // Si el script tiene una URL, la asigna al nuevo script.
            newScript.async = true; // Los scripts se ejecutan de manera asíncrona para no bloquear la carga de la página.
        } else {
            newScript.textContent = oldScript.textContent; // Si el script es inline, copia el contenido del script.
        }
        document.body.appendChild(newScript); // Añade el nuevo script al final del <body> para ejecutarlo.
    });
}

/*
    La función clearContent se utiliza para limpiar el contenido del <main> cuando el usuario está a punto de abandonar la página.
    Esto asegura que el contenido se elimine antes de salir, evitando que la información quede en la página.
*/
function clearContent() {
    document.querySelector('main').innerHTML = ''; // Elimina todo el contenido dentro del <main>.
    console.log("Contenido eliminado al salir de la página."); // Muestra un mensaje de confirmación en la consola.
}
