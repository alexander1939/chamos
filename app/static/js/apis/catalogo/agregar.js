document.addEventListener("DOMContentLoaded", () => {
    if (!estaEnAgregar()) return;  // Verifica si estamos en la página correcta

    iniciarAgregar();  // Llama a la función para mostrar el formulario
});

function iniciarAgregar() {
    const modulo = obtenerModulo();
    if (!modulo) return;

    mostrarFormularioAgregar(modulo);
}

function estaEnAgregar() {
    const path = window.location.pathname.replace(/\/$/, ""); // Elimina la barra final si existe
    const pathSegments = path.split("/");
    const esAgregar = pathSegments.length === 3 && pathSegments[1] === "catalogo" && pathSegments[2] !== "" && pathSegments[2] !== "agregar";

    console.log("Verificando página agregar: ", window.location.pathname, "Resultado:", esAgregar);
    return esAgregar;
}


function obtenerModulo() {
    const pathSegments = window.location.pathname.split("/");
    return pathSegments[2] || null;  // Extrae el módulo desde la URL
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
        <label for="nombre">Nombre de ${modulo}</label>
        <input type="text" class="form-control" id="nombre" name="nombre" required>
    `;

    // Campo para la descripción
    const descripcionGroup = document.createElement("div");
    descripcionGroup.className = "form-group";
    descripcionGroup.innerHTML = `
        <label for="descripcion">Descripción de ${modulo}</label>
        <textarea class="form-control" id="descripcion" name="descripcion" rows="3" required></textarea>
    `;

    // Botón de enviar
    const submitButton = document.createElement("button");
    submitButton.type = "submit";
    submitButton.className = "btn btn-primary mt-3";
    submitButton.textContent = `Agregar ${modulo}`;

    // Agregar elementos al formulario
    form.appendChild(nombreGroup);
    form.appendChild(descripcionGroup);
    form.appendChild(submitButton);

    // Agregar el título, la descripción y el formulario al contenedor
    contentContainer.appendChild(titulo);
    contentContainer.appendChild(descripcion);
    contentContainer.appendChild(form);

    // Manejar el envío del formulario (solo muestra mensaje, sin enviar datos)
    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const nombre = document.getElementById("nombre").value;
        const descripcion = document.getElementById("descripcion").value;

        if (!nombre || !descripcion) {
            mostrarError("Debe proporcionar nombre y descripción.");
            return;
        }

        alert(`Formulario enviado (pero no se hace ninguna petición aún).\n\nNombre: ${nombre}\nDescripción: ${descripcion}`);
    });
}

function mostrarError(error) {
    const contentContainer = document.getElementById("content-container");

    // Remover mensajes de error previos
    const errorPrevio = document.getElementById("error-message");
    if (errorPrevio) {
        errorPrevio.remove();
    }

    const errorMessage = document.createElement("p");
    errorMessage.id = "error-message";
    errorMessage.style.color = "red";
    errorMessage.style.textAlign = "center";
    errorMessage.textContent = error;

    contentContainer.appendChild(errorMessage);
}
