document.addEventListener("DOMContentLoaded", () => {
    inicializarAgregar();
});

// 🔹 Capturar clic en el botón de agregar
function inicializarAgregar() {
    document.body.addEventListener("click", (e) => {
        const botonAgregar = e.target.closest(".btn-agregar");
        if (botonAgregar) {
            e.preventDefault(); // Evita la navegación o recarga de la página

            const modulo = botonAgregar.getAttribute("data-modulo");
            if (modulo) {
                mostrarFormularioAgregar(modulo);
            }
        }
    });
}

// 🔹 Función para mostrar el formulario en el contenedor sin recargar
function mostrarFormularioAgregar(modulo) {
    const contentContainer = document.getElementById("content-container");
    if (!contentContainer) return;

    contentContainer.innerHTML = ""; // Limpia el contenido actual

    // Crear título y descripción
    const titulo = document.createElement("h2");
    titulo.className = "display-4 text-primary text-center";
    titulo.textContent = `Agregar Nuevo ${modulo}`;

    const descripcion = document.createElement("p");
    descripcion.className = "lead text-muted text-center";
    descripcion.textContent = `Aquí puedes agregar un nuevo ${modulo.toLowerCase()}.`;

    // Crear formulario
    const form = document.createElement("form");
    form.id = "form-agregar";
    form.className = "mt-4";

    form.innerHTML = `
        <div class="form-group">
            <label for="nombre">Nombre de ${modulo}</label>
            <input type="text" class="form-control" id="nombre" name="nombre" required>
        </div>
        <div class="form-group">
            <label for="descripcion">Descripción de ${modulo}</label>
            <textarea class="form-control" id="descripcion" name="descripcion" rows="3" required></textarea>
        </div>
        <button type="submit" class="btn btn-primary mt-3">Agregar ${modulo}</button>
    `;

    // Agregar elementos al contenedor
    contentContainer.appendChild(titulo);
    contentContainer.appendChild(descripcion);
    contentContainer.appendChild(form);

    // 🔹 Manejar el envío del formulario
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        await enviarFormularioAgregar(modulo);
    });
}

// 🔹 Función para enviar datos a la API sin recargar
async function enviarFormularioAgregar(modulo) {
    const nombre = document.getElementById("nombre").value;
    const descripcion = document.getElementById("descripcion").value;

    if (!nombre || !descripcion) {
        mostrarError("Debe proporcionar nombre y descripción.");
        return;
    }

    try {
        const response = await fetch(`/api/catalogo/agregar/?modulo=${modulo}`, {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nombre, descripcion })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Error desconocido al agregar.");
        }

        alert(`${modulo.slice(0, -1)} agregado con éxito.`);

        // 🔹 Opcional: Recargar solo la lista del catálogo sin recargar toda la página
        cargarCatalogo(modulo);

    } catch (error) {
        console.error("Error al agregar:", error);
        mostrarError(error.message);
    }
}

// 🔹 Mostrar error en pantalla
function mostrarError(error) {
    const contentContainer = document.getElementById("content-container");

    // Remover errores previos
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
