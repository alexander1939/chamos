/* 
   Este bloque de código se ejecuta cuando el DOM está completamente cargado.
   Verifica si la página actual está en la sección de usuarios, y si es así, 
   llama a la función para obtener y mostrar los usuarios.
*/
document.addEventListener("DOMContentLoaded", () => {
    if (!estaEnUsuarios()) return;  /* Verifica si estamos en la sección de usuarios */

    obtenerUsuarios()  /* Llama a la función que obtiene los usuarios */
        .then(data => mostrarUsuarios(data))  /* Si la obtención es exitosa, muestra los usuarios */
        .catch(error => mostrarError(error));  /* Si ocurre un error, lo muestra */
});

/*
   Esta función realiza el mismo proceso que el bloque anterior, 
   pero puede ser llamada en otros contextos si es necesario.
*/
function iniciarUsuarios() {
    if (!estaEnUsuarios()) return;  /* Verifica si estamos en la sección de usuarios */

    obtenerUsuarios()  /* Llama a la función para obtener usuarios */
        .then(data => mostrarUsuarios(data))  /* Muestra los usuarios obtenidos */
        .catch(error => mostrarError(error));  /* Muestra un error si ocurre */
}

/* 
   Esta función verifica si la página actual corresponde a la sección de usuarios 
   (ya sea en la ruta principal o en una ruta que comience con "/home").
*/
function estaEnUsuarios() {
    return window.location.pathname === "/" || window.location.pathname.startsWith("/home");
}

/* 
   Verifica si el DOM ya ha sido cargado; si es así, ejecuta la función `iniciarUsuarios`.
   Si aún no está cargado, espera a que lo esté y luego ejecuta `iniciarUsuarios`.
*/
if (document.readyState !== "loading") {
    iniciarUsuarios();  /* Si el DOM ya está cargado, inicia la obtención de usuarios */
} else {
    document.addEventListener("DOMContentLoaded", iniciarUsuarios);  /* Espera hasta que el DOM se cargue */
}

/* 
   Esta es una función asincrónica que obtiene los usuarios desde un servidor 
   mediante una solicitud HTTP GET.
*/
async function obtenerUsuarios() {
    const response = await fetch("/api/users/", {
        method: "GET",  /* Método de la solicitud: GET */
        credentials: "include",  /* Incluye las cookies en la solicitud */
        headers: { "Content-Type": "application/json" }  /* Indica que la respuesta será en formato JSON */
    });

    if (!response.ok) {  /* Si la respuesta no es exitosa, lanza un error */
        throw new Error(`Error al obtener usuarios: ${response.statusText}`);
    }

    return response.json();  /* Devuelve la respuesta en formato JSON (lista de usuarios) */
}

/* 
   Esta función muestra los usuarios obtenidos en el DOM.
   Crea los elementos necesarios para mostrarlos correctamente.
*/
function mostrarUsuarios(users) {
    const contentContainer = document.getElementById("content-container");  /* Contenedor donde se mostrarán los usuarios */
    contentContainer.innerHTML = "";  /* Limpiar cualquier contenido previo */

    /* Si no hay usuarios o el arreglo está vacío, muestra un mensaje de error */
    if (!Array.isArray(users) || users.length === 0) {
        mostrarError("No hay usuarios registrados.");
        return;
    }

    /* Crea y agrega el título y la descripción de la sección */
    const titulo = document.createElement("h2");
    titulo.className = "display-4 text-primary text-center";
    titulo.textContent = "Usuarios Registrados";

    const descripcion = document.createElement("p");
    descripcion.className = "lead text-muted text-center";
    descripcion.textContent = "Lista de usuarios registrados en el sistema.";

    contentContainer.appendChild(titulo);  /* Agrega el título al contenedor */
    contentContainer.appendChild(descripcion);  /* Agrega la descripción al contenedor */

    /* Crea un contenedor para las tarjetas de los usuarios */
    const userContainer = document.createElement("div");
    userContainer.className = "row row-cols-1 row-cols-md-3 g-4";
    contentContainer.appendChild(userContainer);

    /* Crea una tarjeta para cada usuario y la agrega al contenedor de usuarios */
    users.forEach(user => {
        userContainer.appendChild(crearTarjetaUsuario(user));
    });
}

/* 
   Esta función crea una tarjeta HTML con la información de un usuario específico.
   La tarjeta contiene su nombre, correo, teléfono y privilegios.
*/
function crearTarjetaUsuario(user) {
    const col = document.createElement("div");
    col.className = "col content-item";
    col.innerHTML = `  <!-- Estructura HTML para cada tarjeta de usuario -->
        <div class="card shadow-sm border-light rounded">
            <div class="card-body">
                <h5 class="card-title">${user.name} ${user.surnames}</h5>
                <p class="card-text"><strong>Correo:</strong> ${user.email}</p>
                <p class="card-text"><strong>Teléfono:</strong> ${user.phone}</p>
                <p class="card-text"><strong>Privilegios:</strong></p>
                <ul>
                    ${Array.isArray(user.privileges) && user.privileges.length > 0
            ? user.privileges.map(priv => `<li>${priv.name}</li>`).join("")
            : "<li>Sin privilegios</li>"}
                </ul>
            </div>
        </div>
    `;
    return col;  /* Devuelve el elemento con la tarjeta del usuario */
}

/* 
   Esta función muestra un mensaje de error en el contenedor principal del DOM.
   Si no se encuentra el contenedor, muestra el error en la consola.
*/
function mostrarError(error) {
    const contentContainer = document.getElementById("content-container");
    if (!contentContainer) {
        console.error("Error: No se encontró el elemento #content-container en el DOM.");
        return;
    }
    contentContainer.innerHTML = `<p style="color: red;">${error}</p>`;  /* Muestra el error en el DOM */
}
