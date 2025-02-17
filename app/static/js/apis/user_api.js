document.addEventListener("DOMContentLoaded", async () => {
    await esperarCargaMenu(); // Espera a que el menú se cargue completamente

    // Verifica si la ruta actual es "/"
    if (window.location.pathname === "/") {
        await cargarUsuarios(); // Carga los usuarios si la ruta es "/"
    }

    inicializarUsuarios(); // Inicializa el evento de clic en el enlace de inicio

    // Maneja el botón "Atrás" del navegador sin recargar la página
    window.addEventListener("popstate", () => {
        if (window.location.pathname === "/") {
            cargarUsuarios();
        }
    });
});

// 🔹 Función para cargar los usuarios
async function cargarUsuarios() {
    const usuarios = await obtenerUsuarios(); // Obtiene los usuarios del backend.
    if (usuarios.error) {
        mostrarMensaje(usuarios.error);
    } else {
        mostrarUsuarios(usuarios); // Muestra los usuarios en el contenedor.
    }
}

// 🔹 Función para esperar a que el menú se cargue dinámicamente
async function esperarCargaMenu() {
    return new Promise((resolve) => {
        const observer = new MutationObserver(() => {
            const homeLink = document.querySelector(".home-link");
            if (homeLink) {
                observer.disconnect(); // Detener la observación cuando se encuentra el elemento
                resolve();
            }
        });

        observer.observe(document.body, { childList: true, subtree: true });
    });
}

// 🔹 Función para inicializar los eventos en "Inicio"
function inicializarUsuarios() {
    const homeLink = document.querySelector(".home-link"); // Buscar el enlace de inicio
    const contentContainer = document.getElementById("content-container");

    if (!homeLink || !contentContainer) {
        console.error("Elementos de usuario no encontrados en el DOM.");
        return;
    }

    // Evento para manejar el clic en el enlace de inicio.
    homeLink.addEventListener("click", async (e) => {
        e.preventDefault(); // Evita la recarga de la página
        window.history.pushState({}, '', '/'); // 🔹 Actualiza la URL sin recargar
        await cargarUsuarios(); // Carga los usuarios
    });
}

// 🔹 Función para obtener los usuarios desde el backend.
async function obtenerUsuarios() {
    try {
        const response = await fetch("/api/users/", {
            method: "GET",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
        });

        if (!response.ok) {
            throw new Error(`Error al obtener usuarios (Código ${response.status}): ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error("Error al obtener los usuarios:", error);
        return { error: "Error al conectar con el servidor." };
    }
}

// 🔹 Función para mostrar los usuarios en el DOM.
function mostrarUsuarios(users) {
    const contentContainer = document.getElementById("content-container");

    if (!Array.isArray(users) || users.length === 0) {
        mostrarMensaje("No hay usuarios registrados.");
        return;
    }

    const userContainer = document.createElement("div");
    userContainer.classList.add("row", "row-cols-1", "row-cols-md-3", "g-4");

    users.forEach(user => {
        const col = document.createElement("div");
        col.classList.add("col", "content-item");

        col.innerHTML = `
            <div class="card shadow-sm border-light rounded">
                <div class="card-body">
                    <h5 class="card-title">${user.name} ${user.surnames}</h5>
                    <p class="card-text"><strong>Correo:</strong> ${user.email}</p>
                    <p class="card-text"><strong>Teléfono:</strong> ${user.phone}</p>
                    <p class="card-text"><strong>Privilegios:</strong></p>
                    <ul>
                        ${Array.isArray(user.privileges) && user.privileges.length > 0
                ? user.privileges.map(priv => `<li>${priv.name}</li>`).join("")
                : "<li>Sin privilegios</li>"}
                    </ul>
                </div>
            </div>
        `;

        userContainer.appendChild(col);
    });

    contentContainer.innerHTML = "";
    contentContainer.appendChild(userContainer);
}

// 🔹 Función para mostrar mensajes de error o información en el contenedor.
function mostrarMensaje(mensaje) {
    const contentContainer = document.getElementById("content-container");
    contentContainer.innerHTML = `<p>${mensaje}</p>`;
}
