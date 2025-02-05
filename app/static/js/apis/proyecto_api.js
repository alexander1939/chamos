document.addEventListener("DOMContentLoaded", function () {
    cargarProyectos(); // Cargar proyectos al iniciar la página

    // Manejar envío del formulario para agregar un proyecto
    const formAgregar = document.getElementById("form-agregar-proyecto");
    if (formAgregar) {
        formAgregar.addEventListener("submit", function (event) {
            event.preventDefault();
            agregarProyecto();
        });
    }
});

// 📌 Función para cargar los proyectos desde la API
function cargarProyectos() {
    fetch("/proyectos/")
        .then(response => response.json())
        .then(data => {
            const listaProyectos = document.getElementById("lista-proyectos");
            if (!listaProyectos) return;

            listaProyectos.innerHTML = ""; // Limpiar la lista antes de cargar

            if (data.message) {
                listaProyectos.innerHTML = `<p>${data.message}</p>`;
                return;
            }

            data.forEach(proyecto => {
                const item = document.createElement("li");
                item.innerHTML = `
                    <strong>${proyecto.nombre}</strong> - ${proyecto.descripcion}
                    <button onclick="editarProyecto(${proyecto.id})">✏ Editar</button>
                    <button onclick="eliminarProyecto(${proyecto.id})">🗑 Eliminar</button>
                `;
                listaProyectos.appendChild(item);
            });
        })
        .catch(error => console.error("Error al cargar proyectos:", error));
}

// 📌 Función para agregar un nuevo proyecto
function agregarProyecto() {
    const nombre = document.getElementById("nombre-proyecto").value;
    const descripcion = document.getElementById("descripcion-proyecto").value;

    fetch("/proyectos/agregar/", {
        method: "POST",
        body: new URLSearchParams({ nombre, descripcion }),
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        }
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url; // Redirigir después de agregar
        }
    })
    .catch(error => console.error("Error al agregar proyecto:", error));
}

// 📌 Función para redirigir al formulario de edición
function editarProyecto(id) {
    window.location.href = `/proyectos/editar/${id}/`;
}

// 📌 Función para eliminar un proyecto con confirmación
function eliminarProyecto(id) {
    if (confirm("¿Estás seguro de que deseas eliminar este proyecto?")) {
        fetch(`/proyectos/eliminar/${id}/`, {
            method: "POST"
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url; // Redirigir después de eliminar
            }
        })
        .catch(error => console.error("Error al eliminar proyecto:", error));
    }
}
