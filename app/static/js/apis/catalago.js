/*
    Este bloque de código espera que el contenido del DOM se cargue completamente antes de ejecutar cualquier acción. 
    El evento "DOMContentLoaded" es disparado cuando el DOM ha terminado de cargarse, 
    pero no necesariamente las imágenes o los recursos externos. 
    Esto asegura que el código que depende del DOM pueda ser ejecutado sin problemas.
    Luego, se obtiene el módulo desde la URL utilizando la función obtenerModulo(). 
    Si no se obtiene un módulo válido, la ejecución se detiene con `return`.
*/
document.addEventListener("DOMContentLoaded", () => {
    const modulo = obtenerModulo();
    if (!modulo) return;

    obtenerDatos(modulo)
        .then(data => mostrarDatos(data, modulo))
        .catch(error => mostrarError(error));
});

/*
    La función iniciarCatalogo() realiza la misma lógica que el bloque anterior, 
    pero en lugar de depender del evento DOMContentLoaded, la función se puede ejecutar en cualquier momento.
    Esto permite reutilizar la lógica para iniciar el catálogo desde otros lugares en el código si es necesario.
    Similar a lo que ocurre en el bloque anterior, la función obtiene el módulo desde la URL 
    y luego hace una solicitud al servidor para obtener los datos asociados a ese módulo.
*/
function iniciarCatalogo() {
    const modulo = obtenerModulo();
    if (!modulo) return;

    const moduloActual = sessionStorage.getItem("modulo_actual");
    const datosAlmacenados = sessionStorage.getItem("datos_modulo");

    if (moduloActual === modulo && datosAlmacenados) {
        console.log(`Los datos de ${modulo} ya están cargados. Mostrando desde cache.`);
        mostrarDatos(JSON.parse(datosAlmacenados), modulo); // Usa los datos almacenados
        return;
    }

    obtenerDatos(modulo)
        .then(data => {
            mostrarDatos(data, modulo);
            sessionStorage.setItem("modulo_actual", modulo);
            sessionStorage.setItem("datos_modulo", JSON.stringify(data)); // Guarda los datos en cache
        })
        .catch(error => mostrarError(error));
}

/*
    La función obtenerModulo() se encarga de extraer el módulo actual desde la URL de la página.
    Esto es útil para identificar en qué sección o categoría se encuentra el usuario, como "materias", "proyectos", "juegos", etc.
*/

function obtenerModulo() {
    const pathSegments = window.location.pathname.split("/");
    return pathSegments[2] || null; // Obtiene el módulo de la URL (materias, proyectos, juegos)
}

/*
    Este bloque verifica si el documento ya está completamente cargado utilizando `document.readyState`.
    Si el documento ya está en estado "loading", entonces la función `iniciarCatalogo()` se ejecutará inmediatamente.
    Si no, se agrega un listener para ejecutar la función cuando el DOM esté listo, 
    asegurando que el catálogo se inicie correctamente solo después de que el contenido de la página esté disponible.
*/
if (document.readyState !== "loading") {
    iniciarCatalogo();
} else {
    document.addEventListener("DOMContentLoaded", iniciarCatalogo);
}

/*
    La función obtenerModulo() toma la URL del navegador, la divide en segmentos utilizando `/` como delimitador, 
    y retorna el tercer segmento, que corresponde al "módulo". 
    Si el segmento no existe, devuelve `null`. Esta función es útil para obtener dinámicamente el módulo 
    actual basado en la ruta de la URL.
*/
function obtenerModulo() {
    const pathSegments = window.location.pathname.split("/");
    return pathSegments[2] || null;
}

/*
    La función obtenerDatos es asíncrona y se encarga de hacer una solicitud HTTP GET al servidor
    para obtener los datos asociados al módulo especificado. 
    Utiliza `fetch` para realizar la solicitud y espera la respuesta. 
    Si la respuesta es correcta (status 200), convierte la respuesta a formato JSON y la retorna. 
    Si la respuesta es un error, se lanza una excepción con el mensaje de error correspondiente.
*/
async function obtenerDatos(modulo) {
    const response = await fetch(`/api/catalogo/?modulo=${modulo}`, {
        method: "GET",
        credentials: "include"
    });

    if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
    }

    return response.json();
}

/*
    La función mostrarDatos es responsable de renderizar los datos recibidos en la interfaz de usuario. 
    Limpia el contenedor de contenido antes de mostrar los nuevos datos. 
    Si los datos no contienen la información esperada (materias, proyectos o juegos), o si no hay datos disponibles, 
    muestra un mensaje de error. Si los datos son válidos, crea y muestra tarjetas para cada elemento.
*/
function mostrarDatos(data, modulo) {
    const contentContainer = document.getElementById("content-container");
    contentContainer.innerHTML = ""; // Limpia el contenedor

    if (!data || data.error || !data.materias && !data.proyectos && !data.juegos) {
        mostrarError("No se encontraron datos.");
        return;
    }

    const items = data.materias || data.proyectos || data.juegos;
    if (items.length === 0) {
        mostrarError("No hay registros disponibles.");
        return;
    }

    // Crear el título y la descripción del módulo dinámicamente
    const titulo = document.createElement("h2");
    titulo.className = "display-4 text-primary text-center";
    titulo.textContent = `${modulo} Registrados`;

    const descripcion = document.createElement("p");
    descripcion.className = "lead text-muted text-center";
    descripcion.textContent = `Aquí puedes ver todos los ${modulo.toLowerCase()} registrados.`;

    // Agregar el título y la descripción al contenedor
    contentContainer.appendChild(titulo);
    contentContainer.appendChild(descripcion);

    // Crear un contenedor para las tarjetas
    const cardContainer = document.createElement("div");
    cardContainer.className = "row row-cols-1 row-cols-md-3 g-4";
    contentContainer.appendChild(cardContainer);

    // Renderizar las tarjetas
    items.forEach(item => {
        cardContainer.appendChild(crearTarjeta(item, modulo, data));
    });

    // Mostrar el botón de agregar si hay permisos
    if (data.can_create) {
        const addButton = document.createElement("a");
        addButton.href = `/catalogo/agregar/${modulo}`;
        addButton.className = "btn btn-success btn-lg";
        addButton.textContent = `Agregar Nuevo ${modulo.slice(0, -1)}`;

        const addButtonContainer = document.createElement("div");
        addButtonContainer.className = "text-center mt-4";
        addButtonContainer.appendChild(addButton);

        contentContainer.appendChild(addButtonContainer);
    }
}

/*
    La función crearTarjeta crea un elemento de tarjeta en HTML para cada item (materia, proyecto o juego),
    llenando sus detalles como nombre y descripción. 
    Si los datos contienen permisos para editar o eliminar (can_edit, can_delete), se incluyen los botones correspondientes.
    Los botones de "Ver Detalles", "Editar" y "Eliminar" están condicionados según los permisos disponibles.
*/
function crearTarjeta(item, modulo, data) {
    const col = document.createElement("div");
    col.className = "col content-item";
    col.innerHTML = `
        <div class="card shadow-sm border-light rounded">
            <div class="card-body">
                <h5 class="card-title">${item.nombre}</h5>
                <p class="card-text">${item.descripcion}</p>
                <div class="d-flex justify-content-between align-items-center">
                    <a href="/catalogo/${modulo}/${item.id}" class="btn btn-primary btn-sm">Ver Detalles</a>
                    <div class="d-flex">
                        ${data.can_edit ? `
                        <a href="#" class="btn btn-warning btn-sm me-2">
                            <img src="/static/images/edit.png" alt="Editar" width="20" height="20">
                        </a>` : ""}
                        ${data.can_delete ? `
                        <form action="/catalo/eliminar/${modulo}/${item.id}" method="POST" style="display:inline-block;">
                            <button type="submit" class="btn btn-danger btn-sm">
                                <img src="/static/images/delete.png" alt="Eliminar" width="20" height="20">
                            </button>
                        </form>` : ""}
                    </div>
                </div>
            </div>
        </div>
    `;
    return col;
}

/*
    La función mostrarError es responsable de mostrar un mensaje de error en el contenedor de contenido.
    Si no se encuentra el contenedor, se registra un error en la consola. Si se encuentra, se muestra el mensaje de error 
    en color rojo. Esto se utiliza para informar al usuario cuando no hay datos disponibles o cuando ocurre algún error.
*/
function mostrarError(error) {
    const contentContainer = document.getElementById("content-container");
    if (!contentContainer) {
        console.error("Error: No se encontró el elemento #content-container en el DOM.");
        return;
    }

    contentContainer.innerHTML = `<p style="color: red;">${error}</p>`;
}
