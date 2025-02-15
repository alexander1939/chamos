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

    obtenerDatos(modulo)
        .then(data => mostrarDatos(data, modulo))
        .catch(error => mostrarError(error));
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
    contentContainer.innerHTML = "";

    if (!data || data.error || !data.materias && !data.proyectos && !data.juegos) {
        mostrarError("No tienes proyectos registrados.");
        return;
    }

    const items = data.materias || data.proyectos || data.juegos;
    if (items.length === 0) {
        mostrarError("No tienes proyectos registrados.");
        return;
    }

    items.forEach(item => {
        contentContainer.appendChild(crearTarjeta(item, modulo, data));
    });
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
                    <a href="/catalogo/${modulo}/detalle/${item.id}" class="btn btn-primary btn-sm">Ver Detalles</a>
                    <div class="d-flex">
                        ${data.can_edit ? `
                        <a href="/catalogo/${modulo}/editar/${item.id}" class="btn btn-warning btn-sm me-2">
                            <img src="/static/images/edit.png" alt="Editar" width="20" height="20">
                        </a>` : ""}
                        ${data.can_delete ? `
                        <form action="/catalogo/${modulo}/eliminar/${item.id}" method="POST" style="display:inline-block;">
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
