document.addEventListener("DOMContentLoaded", () => {
    const modulo = obtenerModulo();
    if (!modulo) return;

    mostrarFormularioAgregar(modulo);
});

function obtenerModulo() {
    const pathSegments = window.location.pathname.split("/");
    return pathSegments[2] || null;
}

function mostrarFormularioAgregar(modulo) {
    const contentContainer = document.getElementById("content-container");
    contentContainer.innerHTML = "";

    // Crear el título y la descripción del módulo dinámicamente
    const titulo = document.createElement("h2");
    titulo.className = "display-4 text-primary text-center";
    titulo.textContent = `Agregar Nuevo ${modulo}`;

    const descripcion = document.createElement("p");
    descripcion.className = "lead text-muted text-center";
    descripcion.textContent = `Aquí puedes agregar un nuevo ${modulo.toLowerCase()}.`;

    // Crear el formulario
    const form = document.createElement("form");
    form.id = "form-agregar";
    form.className = "mt-4";

    // Campo para el nombre
    const nombreGroup = document.createElement("div");
    nombreGroup.className = "form-group";
    nombreGroup.innerHTML = `
        <label for="nombre">Nombre</label>
        <input type="text" class="form-control" id="nombre" name="nombre" required>
    `;

    // Campo para la descripción
    const descripcionGroup = document.createElement("div");
    descripcionGroup.className = "form-group";
    descripcionGroup.innerHTML = `
        <label for="descripcion">Descripción</label>
        <textarea class="form-control" id="descripcion" name="descripcion" rows="3" required></textarea>
    `;

    // Botón de enviar
    const submitButton = document.createElement("button");
    submitButton.type = "submit";
    submitButton.className = "btn btn-primary";
    submitButton.textContent = `Agregar ${modulo}`;

    // Agregar elementos al formulario
    form.appendChild(nombreGroup);
    form.appendChild(descripcionGroup);
    form.appendChild(submitButton);

    // Agregar el título, la descripción y el formulario al contenedor
    contentContainer.appendChild(titulo);
    contentContainer.appendChild(descripcion);
    contentContainer.appendChild(form);

    // Manejar el envío del formulario
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const nombre = document.getElementById("nombre").value;
        const descripcion = document.getElementById("descripcion").value;

        if (!nombre || !descripcion) {
            mostrarError("Debe proporcionar nombre y descripción.");
            return;
        }

        try {
            const response = await agregarContenido(modulo, nombre, descripcion);
            if (response.ok) {
                window.location.href = `/catalogo/${modulo}`; // Redirigir al catálogo después de agregar
            } else {
                const error = await response.json();
                mostrarError(error.error || "Error al agregar el contenido.");
            }
        } catch (error) {
            mostrarError("Error en la solicitud.");
        }
    });
}

async function agregarContenido(modulo, nombre, descripcion) {
    const data = { nombre, descripcion };
    const response = await fetch(`/catalogo/${modulo}/agregar/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"  // Asegúrate de incluir este encabezado
        },
        body: JSON.stringify(data)  // Convierte los datos a JSON
    });
    return response;
}

function mostrarError(error) {
    const contentContainer = document.getElementById("content-container");
    if (!contentContainer) {
        console.error("Error: No se encontró el elemento #content-container en el DOM.");
        return;
    }

    const errorMessage = document.createElement("p");
    errorMessage.style.color = "red";
    errorMessage.textContent = error;

    contentContainer.appendChild(errorMessage);
}