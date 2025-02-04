document.addEventListener("DOMContentLoaded", () => {
    const logoutButton = document.getElementById("logoutButton");

    if (logoutButton) {
        logoutButton.addEventListener("click", async (event) => {
            event.preventDefault(); // Evita que el enlace recargue la página

            try {
                const response = await fetch("/api/logout/", {
                    method: "POST",
                    credentials: "include", // Asegura que se envíen las cookies
                    headers: {
                        "Content-Type": "application/json",
                    },
                });

                if (response.ok) {
                    window.location.href = "/login"; // Redirige a la página de login
                } else {
                    alert("Error al cerrar sesión");
                }
            } catch (error) {
                console.error("Error:", error);
            }
        });
    } else {
        console.error("El botón de logout no fue encontrado en el DOM.");
    }
});
