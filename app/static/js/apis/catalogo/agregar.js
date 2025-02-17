document.addEventListener("DOMContentLoaded", () => {
    inicializarAgregar();
    actualizarBreadcrumbs();
});

function inicializarAgregar() {
    document.body.addEventListener("click", async (e) => {
        const addButton = e.target.closest(".btn-agregar");
        if (addButton) {
            e.preventDefault();
            const modulo = addButton.getAttribute("data-modulo") || addButton.href.split("/").pop();

            if (modulo) {
                history.pushState({}, '', `/catalogo/agregar/${modulo}/`);
                mostrarFormularioAgregar(modulo);
                actualizarBreadcrumbs();
            }
        }
    });
}

function mostrarFormularioAgregar(modulo) {
    const contentContainer = document.getElementById("content-container");
    if (!contentContainer) return;

    contentContainer.innerHTML = "";

    const titulo = document.createElement("h2");
    titulo.className = "display-4 text-primary text-center";
    titulo.textContent = `Agregar Nuevo ${modulo}`;

    const descripcion = document.createElement("p");
    descripcion.className = "lead text-muted text-center";
    descripcion.textContent = `Aquí puedes agregar un nuevo ${modulo.toLowerCase()}.`;

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

    contentContainer.appendChild(titulo);
    contentContainer.appendChild(descripcion);
    contentContainer.appendChild(form);

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        await enviarFormularioAgregar(modulo);
    });
}

async function enviarFormularioAgregar(modulo) {
    const nombre = document.getElementById("nombre").value.trim();
    const descripcion = document.getElementById("descripcion").value.trim();

    if (!nombre || !descripcion) {
        Swal.fire({
            icon: "error",
            title: "Campos incompletos",
            text: "Debe proporcionar nombre y descripción.",
            confirmButtonText: "Entendido"
        });
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

        Swal.fire({
            icon: "success",
            title: "¡Éxito!",
            text: `${modulo.slice(0, -1)} agregado con éxito.`,
            confirmButtonText: "Aceptar"
        }).then(() => {
            history.pushState({}, '', `/catalogo/${modulo}/`);
            cargarCatalogo(modulo);
        });

    } catch (error) {
        console.error("Error al agregar:", error);
        Swal.fire({
            icon: "error",
            title: "Error",
            text: error.message || "No se pudo agregar el elemento.",
            confirmButtonText: "Cerrar"
        });
    }
}
