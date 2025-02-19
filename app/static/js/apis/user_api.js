document.addEventListener("DOMContentLoaded", async () => {
    await esperarCargaMenu();
    if (window.location.pathname === "/") {
        await cargarUsuarios();

    }

    inicializarUsuarios();

    window.addEventListener("popstate", () => {
        if (window.location.pathname === "/") {
            cargarUsuarios();
        }
    });
});

async function cargarUsuarios() {
    const usuarios = await obtenerUsuarios();
    if (usuarios.error) {
        mostrarMensaje(usuarios.error);
    } else {
        mostrarUsuarios(usuarios);
        actualizarBreadcrumbs();
    }
}

async function esperarCargaMenu() {
    return new Promise((resolve) => {
        const observer = new MutationObserver(() => {
            const homeLink = document.querySelector(".home-link");
            if (homeLink) {
                observer.disconnect();
                resolve();
            }
        });

        observer.observe(document.body, { childList: true, subtree: true });
    });
}

function inicializarUsuarios() {
    const homeLink = document.querySelector(".home-link");
    const contentContainer = document.getElementById("content-container");

    if (!homeLink || !contentContainer) {
        console.error("Elementos de usuario no encontrados en el DOM.");
        return;
    }

    homeLink.addEventListener("click", async (e) => {
        e.preventDefault();
        window.history.pushState({}, '', '/');
        await cargarUsuarios();
    });
}

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

function mostrarMensaje(mensaje) {
    const contentContainer = document.getElementById("content-container");
    contentContainer.innerHTML = `<p>${mensaje}</p>`;
}
