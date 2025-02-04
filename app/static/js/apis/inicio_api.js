document.addEventListener("DOMContentLoaded", async () => {
    const cardsContainer = document.getElementById("cards-container");

    try {
        const response = await fetch("/api/menu", {
            method: "GET",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
        });

        if (!response.ok) {
            if (response.status === 401) {
                console.warn("Sesión expirada o token inválido. Redirigiendo a login...");
                window.location.href = "/login";
            } else {
                console.error(`Error en la API (Código ${response.status}): ${response.statusText}`);
            }
            return;
        }

        const data = await response.json();

        if (!data || typeof data !== "object") {
            console.error("La API devolvió un formato inesperado:", data);
            return;
        }

        if (data.error) {
            console.error("Error en la API:", data.error);
            return;
        }

        if (!Array.isArray(data.privilegios) || data.privilegios.length === 0) {
            console.warn("El usuario no tiene privilegios asignados.");
            return;
        }

        // Generación de cards de forma similar al menú
        data.privilegios.forEach((privilegio) => {
            const items = data.contenido[privilegio] || [];
            cardsContainer.innerHTML += createCard(privilegio, items);
        });

    } catch (error) {
        console.error("Error al conectar con la API del menú:", error);
        alert("No se pudo cargar el contenido. Verifica tu conexión e intenta nuevamente.");
    }
});

function createCard(title, items) {
    let card = `
        <div class="card">
            <h3>${title}</h3>
            <div class="card-content">
    `;

    if (Array.isArray(items) && items.length > 0) {
        items.forEach((item) => {
            card += `<p class="item" onclick="redirectTo('${title}', '${item.nombre}')">${item.nombre}</p>`;
        });
    } else {
        card += `<p class="no-items">No hay elementos disponibles</p>`;
    }

    card += `</div></div>`;
    return card;
}

function redirectTo(title, itemName) {
    window.location.href = `/${title.toLowerCase()}/${itemName.toLowerCase()}`;
}
