document.addEventListener("DOMContentLoaded", () => {
    const logoutButton = document.getElementById("logoutButton");

    if (logoutButton) {
        logoutButton.addEventListener("click", async (event) => {
            event.preventDefault();

            try {
                const response = await fetch("/api/logout/", {
                    method: "POST",
                    credentials: "include",
                    headers: {
                        "Content-Type": "application/json",
                    },
                });

                if (response.ok) {
                    window.location.href = "/login";
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
