document.addEventListener("DOMContentLoaded", async () => {
    await loadSessions(); // Carga las sesiones al cargar la página

    document.addEventListener("click", async (event) => {
        if (event.target.classList.contains("delete-session")) {
            const sessionId = event.target.getAttribute("data-session-id");
            await deleteSession(sessionId);
        }
    });
});

async function loadSessions() {
    try {
        const response = await fetch("/api/active/");
        if (!response.ok) throw new Error("Error al cargar sesiones.");

        const sessions = await response.json();
        console.log("Sesiones obtenidas:", sessions); // <-- Verifica si se reciben los datos

        const tableBody = document.querySelector("#sessionsTable tbody");
        tableBody.innerHTML = ""; // Limpiar tabla antes de agregar los datos

        sessions.forEach(session => {
            const row = document.createElement("tr");
            row.id = `session-${session.id}`;
            row.innerHTML = `
                <td>${session.id}</td>
                <td>${session.ip_address}</td>
                <td>${session.user_agent}</td>
                <td>${session.created_at}</td>
                <td>
                    <button class="btn btn-danger delete-session" data-session-id="${session.id}">Eliminar</button>
                </td>
            `;
            tableBody.appendChild(row);
        });

    } catch (error) {
        console.error("Error cargando sesiones:", error);
        alert("No se pudieron cargar las sesiones.");
    }
}


async function deleteSession(sessionId) {
    try {
        const response = await fetch(`/api/sessions/${sessionId}/`, {
            method: 'DELETE',
            credentials: 'include'  // Para enviar cookies como el token de autenticación
        });

        if (response.ok) {
            document.getElementById(`session-${sessionId}`).remove();
            alert("Sesión eliminada correctamente.");
        } else {
            const errorData = await response.json();
            alert(`Error: ${errorData.error || "No se pudo eliminar la sesión"}`);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Hubo un problema al eliminar la sesión.");
    }
}
