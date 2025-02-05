document.addEventListener("DOMContentLoaded", function () {
    cargarMaterias(); // Cargar materias al iniciar la página

    // Manejar envío del formulario para agregar materia
    const formAgregar = document.getElementById("form-agregar");
    if (formAgregar) {
        formAgregar.addEventListener("submit", function (event) {
            event.preventDefault();
            agregarMateria();
        });
    }
});

// 📌 Función para cargar las materias desde la API
function cargarMaterias() {
    fetch("/materias/")
        .then(response => response.json())
        .then(data => {
            const listaMaterias = document.getElementById("lista-materias");
            if (!listaMaterias) return;

            listaMaterias.innerHTML = ""; // Limpiar la lista antes de cargar

            if (data.message) {
                listaMaterias.innerHTML = `<p>${data.message}</p>`;
                return;
            }

            data.forEach(materia => {
                const item = document.createElement("li");
                item.innerHTML = `
                    <strong>${materia.nombre}</strong> - ${materia.descripcion}
                    <button onclick="editarMateria(${materia.id})">✏ Editar</button>
                    <button onclick="eliminarMateria(${materia.id})">🗑 Eliminar</button>
                `;
                listaMaterias.appendChild(item);
            });
        })
        .catch(error => console.error("Error al cargar materias:", error));
}

// 📌 Función para agregar una materia
function agregarMateria() {
    const nombre = document.getElementById("nombre").value;
    const descripcion = document.getElementById("descripcion").value;

    fetch("/materias/agregar/", {
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
    .catch(error => console.error("Error al agregar materia:", error));
}

// 📌 Función para redirigir al formulario de edición
function editarMateria(id) {
    window.location.href = `/materias/editar/${id}/`;
}

// 📌 Función para eliminar una materia con confirmación
function eliminarMateria(id) {
    if (confirm("¿Estás seguro de que deseas eliminar esta materia?")) {
        fetch(`/materias/eliminar/${id}/`, {
            method: "POST"
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url; // Redirigir después de eliminar
            }
        })
        .catch(error => console.error("Error al eliminar materia:", error));
    }
}
