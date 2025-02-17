
/*
Inicializa la funcionalidad de agregar elementos:
1. Escucha clics en botones con clase "btn-agregar".
2. Obtiene el módulo y actualiza la URL.
3. Muestra el formulario para agregar un nuevo elemento.
*/
document.addEventListener("DOMContentLoaded", () => {
    const itemId = obtenerItemId();
    if (itemId) {
        return;
    }

    inicializarCatalogo();

    const modulo = obtenerModulo();
    if (modulo) {
        cargarCatalogo(modulo);
    }

    window.addEventListener("popstate", () => {
        const modulo = obtenerModulo();
        if (modulo) {
            cargarCatalogo(modulo);
        }
    });

});

/*
Función que inicializa el catálogo:
1. Escucha los clics en los enlaces con clase "list-link".
2. Evita el comportamiento por defecto (navegar a un enlace).
3. Actualiza la URL con el módulo seleccionado.
4. Carga el catálogo del módulo seleccionado.
*/
function inicializarCatalogo() {
    document.body.addEventListener("click", async (e) => {
        const link = e.target.closest(".list-link");
        if (link) {
            e.preventDefault();

            const modulo = link.getAttribute("data-modulo");
            if (modulo) {
                window.history.pushState({}, '', `/catalogo/${modulo}/`);
                await cargarCatalogo(modulo);
            }
        }
    });
}


/*
Obtiene el módulo actual desde la URL:
1. Divide la ruta de la URL en segmentos.
2. Devuelve el segundo segmento (el módulo).
3. Si no existe, retorna null.
*/
function obtenerModulo() {
    const pathSegments = window.location.pathname.split("/");
    return pathSegments[2] || null;
}

/*
Obtiene los datos del catálogo para un módulo específico:
1. Realiza una petición GET a la API con el módulo.
2. Si la respuesta es exitosa, devuelve los datos en formato JSON.
3. Si ocurre un error, lo maneja y muestra un mensaje de error.
*/
async function obtenerDatos(modulo) {
    try {
        const response = await fetch(`/api/catalogo/?modulo=${modulo}`, {
            method: "GET",
            credentials: "include"
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error("Error al obtener el catálogo:", error);
        return { error: "Error al conectar con el servidor." };
    }
}

/*
Carga el catálogo para un módulo específico:
1. Obtiene el contenedor donde se mostrará el catálogo.
2. Muestra un mensaje de "Cargando..." mientras se obtienen los datos.
3. Si los datos son correctos, los muestra.
4. Si ocurre un error, muestra un mensaje de error.
*/
async function cargarCatalogo(modulo) {
    if (!modulo || window.location.pathname.includes("agregar")) return;

    try {
        const contentContainer = document.getElementById("content-container");
        if (!contentContainer) {
            console.error("Error: No se encontró el #content-container en el DOM.");
            return;
        }

        contentContainer.innerHTML = `<p>Cargando ${modulo}...</p>`;
        const data = await obtenerDatos(modulo);
        if (data.error) {
            mostrarError(data.error);
        } else {
            mostrarDatos(data, modulo);
            actualizarBreadcrumbs();

        }
    } catch (error) {
        mostrarError("Error al cargar el catálogo.");
    }
}


/*
Muestra los datos del catálogo en el contenedor correspondiente:
1. Crea el título y la descripción dinámicamente.
2. Crea las tarjetas para cada elemento del catálogo.
3. Si se puede agregar un nuevo elemento, muestra el botón para agregar.
*/
function mostrarDatos(data, modulo) {
    const contentContainer = document.getElementById("content-container");
    contentContainer.innerHTML = "";
    if (!data || data.error || (!data.materias && !data.proyectos && !data.juegos)) {
        mostrarError("No se encontraron datos.");
        return;
    }

    const items = data.materias || data.proyectos || data.juegos;
    if (items.length === 0) {
        mostrarError("No hay registros disponibles.");
        return;
    }

    // Título y descripción dinámicos
    const titulo = document.createElement("h2");
    titulo.className = "display-4 text-primary text-center";
    titulo.textContent = `${modulo} Registrados`;

    const descripcion = document.createElement("p");
    descripcion.className = "lead text-muted text-center";
    descripcion.textContent = `Aquí puedes ver todos los ${modulo.toLowerCase()} registrados.`;

    contentContainer.appendChild(titulo);
    contentContainer.appendChild(descripcion);

    const cardContainer = document.createElement("div");
    cardContainer.className = "row row-cols-1 row-cols-md-3 g-4";
    contentContainer.appendChild(cardContainer);

    items.forEach(item => {
        cardContainer.appendChild(crearTarjeta(item, modulo, data));
    });

    if (data.can_create) {
        const addButton = document.createElement("a");
        addButton.href = `/catalogo/agregar/${modulo}/`;
        addButton.className = "btn btn-success btn-lg btn-agregar";
        addButton.textContent = `Agregar Nuevo ${modulo.slice(0, -1)}`;

        addButton.setAttribute("data-modulo", modulo);

        const addButtonContainer = document.createElement("div");
        addButtonContainer.className = "text-center mt-4";
        addButtonContainer.appendChild(addButton);

        contentContainer.appendChild(addButtonContainer);
    }

}


function crearTarjeta(item, modulo, data) {
    const col = document.createElement("div");
    col.className = "col content-item";
    col.innerHTML = `
        <div class="card shadow-sm border-light rounded">
            <div class="card-body">
                <h5 class="card-title">${item.nombre}</h5>
                <p class="card-text">${item.descripcion}</p>
                <div class="d-flex justify-content-between align-items-center">
                    <a href="/catalogo/${modulo}/detalle/${item.id}" class="deta-link btn btn-primary btn-sm">Ver Detalles</a>
                    <div class="d-flex">
                        ${data.can_edit ? `
                        <a href="#" class="btn-editar btn btn-warning btn-sm me-2"
                            data-modulo="${modulo}" data-id="${item.id}">
                            <img src="/static/images/edit.png" alt="Editar" width="20" height="20">
                        </a>` : ""}
                        ${data.can_delete ? `
 <button class="btn btn-danger btn-sm btn-eliminar" data-modulo="${modulo}" data-id="${item.id}">
    <img src="/static/images/delete.png" alt="Eliminar" width="20" height="20">
</button>
` : ""}
                    </div>
                </div>
            </div>
        </div>
    `;
    return col;
}

function mostrarError(error) {
    const contentContainer = document.getElementById("content-container");
    if (!contentContainer) {
        console.error("Error: No se encontró el elemento #content-container en el DOM.");
        return;
    }

    contentContainer.innerHTML = `<p style="color: red;">${error}</p>`;
}
