document.addEventListener("DOMContentLoaded", function () {
    cargarJuegos(); // Cargar juegos al iniciar la página

    // Manejar envío del formulario para agregar un juego
    const formAgregar = document.getElementById("form-agregar-juego");
    if (formAgregar) {
        formAgregar.addEventListener("submit", function (event) {
            event.preventDefault();
            agregarJuego();
        });
    }
});

// 📌 Función para cargar los juegos desde la API
function cargarJuegos() {
    fetch("/juegos/")
        .then(response => response.json())
        .then(data => {
            const listaJuegos = document.getElementById("lista-juegos");
            if (!listaJuegos) return;

            listaJuegos.innerHTML = ""; // Limpiar la lista antes de cargar

            if (data.message) {
                listaJuegos.innerHTML = `<p>${data.message}</p>`;
                return;
            }

            data.forEach(juego => {
                const item = document.createElement("li");
                item.innerHTML = `
                    <strong>${juego.nombre}</strong> - ${juego.descripcion}
                    <button onclick="editarJuego(${juego.id})">✏ Editar</button>
                    <button onclick="eliminarJuego(${juego.id})">🗑 Eliminar</button>
                `;
                listaJuegos.appendChild(item);
            });
        })
        .catch(error => console.error("Error al cargar juegos:", error));
}

// 📌 Función para agregar un nuevo juego
function agregarJuego() {
    const nombre = document.getElementById("nombre-juego").value;
    const descripcion = document.getElementById("descripcion-juego").value;

    fetch("/juegos/agregar/", {
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
    .catch(error => console.error("Error al agregar juego:", error));
}

// 📌 Función para redirigir al formulario de edición
function editarJuego(id) {
    window.location.href = `/juegos/editar/${id}/`;
}

// 📌 Función para eliminar un juego con confirmación
function eliminarJuego(id) {
    if (confirm("¿Estás seguro de que deseas eliminar este juego?")) {
        fetch(`/juegos/eliminar/${id}/`, {
            method: "POST"
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url; // Redirigir después de eliminar
            }
        })
        .catch(error => console.error("Error al eliminar juego:", error));
    }
}
