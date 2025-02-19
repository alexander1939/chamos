async function loadUserData() {
    try {
        const response = await fetch("/api/auth/user/", {
            method: "GET",
            credentials: "include"
        });

        if (response.ok) {
            const userData = await response.json();
            const userNameElement = document.getElementById("user-name");
            if (userNameElement) {
                userNameElement.textContent = `${userData.name} ${userData.surnames}`;
            }
        } else {
            console.error("Error al obtener los datos del usuario:", response.statusText);
        }
    } catch (error) {
        console.error("Error al conectar con la API:", error);
    }
}

// Ejecutar la función cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", loadUserData);