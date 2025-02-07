document.addEventListener("DOMContentLoaded", async () => {
    const userCardsContainer = document.getElementById("user-cards");

    try {
        const response = await fetch("/api/users/", {
            method: "GET",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
        });

        if (!response.ok) {
            console.error(`Error al obtener usuarios (Código ${response.status}): ${response.statusText}`);
            return;
        }

        const users = await response.json();
        if (!Array.isArray(users)) {
            console.error("La API no devolvió una lista de usuarios:", users);
            return;
        }

        userCardsContainer.innerHTML = "";
        users.forEach(user => {
            const card = document.createElement("div");
            card.classList.add("card");
            card.dataset.name = `${user.name} ${user.surnames}`;
            card.dataset.email = user.email;
            card.dataset.phone = user.phone;

            card.innerHTML = `
                <div class="card-header">
                    <h2>${user.name} ${user.surnames}</h2>
                </div>
                <div class="card-body">
                    <p><strong>Correo:</strong> ${user.email}</p>
                    <p><strong>Teléfono:</strong> ${user.phone}</p>
                    <p><strong>Privilegios:</strong></p>
                    <ul>
                        ${user.privileges.map(priv => `<li>${priv.name}</li>`).join("")}
                    </ul>
                </div>
            `;

            userCardsContainer.appendChild(card);
        });

    } catch (error) {
        console.error("Error al cargar los usuarios:", error);
    }
});
document.addEventListener("DOMContentLoaded", async () => {
    const userCardsContainer = document.getElementById("user-name");

    try {
        const response = await fetch("/api/users/", {
            method: "GET",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
        });

        if (!response.ok) {
            console.error(`Error al obtener usuarios (Código ${response.status}): ${response.statusText}`);
            return;
        }

        const users = await response.json();
        if (!Array.isArray(users)) {
            console.error("La API no devolvió una lista de usuarios:", users);
            return;
        }

        userCardsContainer.innerHTML = "";
        users.forEach(user => {
            const card = document.createElement("h2");
            card.classList.add("ms-2");
            card.dataset.name = `${user.name} ${user.surnames}`;


            card.innerHTML = `
                
                    <h6>${user.name} ${user.surnames}</h6>
            `;

            userCardsContainer.appendChild(card);
        });

    } catch (error) {
        console.error("Error al cargar los usuarios:", error);
    }
});
