document.addEventListener("DOMContentLoaded", async () => {
    await loadSessions(); 
    await loadSessionSettings(); 

    document.addEventListener("click", async (event) => {
        if (event.target.classList.contains("delete-session")) {
            const sessionId = event.target.getAttribute("data-session-id");
            await deleteSession(sessionId);
        } else if (event.target.id === "toggle-multiple-sessions") {
            await updateMultipleSessions(event.target.checked);
        } else if (event.target.id === "toggle-2fa") {
            await updateEnable2FA(event.target.checked);
        }
    });
});

async function loadSessions() {
    try {
        const response = await fetch("/api/active/");
        if (!response.ok) throw new Error("Error al cargar sesiones.");

        const sessions = await response.json();
        console.log("Sesiones obtenidas:", sessions);

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
            credentials: 'include'
        });

        console.log(`Intentando eliminar sesión: ${sessionId}`);

        if (response.status === 401) {
            console.warn("Sesión cerrada, eliminando cookies y redirigiendo al login...");

            // 🔹 Eliminar cookies manualmente SIN recargar
            document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
            document.cookie = "refresh_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";

            // 🔥 Notificar a la aplicación para cerrar sesión en todas las pestañas
            localStorage.setItem("logout", Date.now());

            window.location.href = "/login";  
            return;
        }

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




async function loadSessionSettings() {
    try {
        const response = await fetch("/api/session-settings/");
        if (!response.ok) throw new Error("Error al obtener configuración de sesión.");

        const settings = await response.json();
        console.log("Configuración actual:", settings);

        document.getElementById("toggle-multiple-sessions").checked = settings.allow_multiple_sessions;
        document.getElementById("toggle-2fa").checked = settings.enable_2fa;
    } catch (error) {
        console.error("Error obteniendo configuración:", error);
        alert("No se pudo cargar la configuración de la sesión.");
    }
}

async function updateMultipleSessions(value) {
    try {
        const response = await fetch("/api/session-settings/multiple-sessions/", {
            method: 'PUT',
            headers: { "Content-Type": "application/json" },
            credentials: 'include',
            body: JSON.stringify({ allow_multiple_sessions: value })
        });

        const result = await response.json();
        if (response.ok) {
            alert("Configuración de sesiones múltiples actualizada.");
        } else {
            alert(`Error: ${result.error || "No se pudo actualizar la configuración."}`);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Hubo un problema al actualizar la configuración.");
    }
}

async function updateEnable2FA(value) {
    try {
        const response = await fetch("/api/session-settings/enable-2fa/", {
            method: 'PUT',
            headers: { "Content-Type": "application/json" },
            credentials: 'include',
            body: JSON.stringify({ enable_2fa: value })
        });

        const result = await response.json();
        if (response.ok) {
            alert("Verificación en dos pasos actualizada.");
        } else {
            alert(`Error: ${result.error || "No se pudo actualizar la configuración."}`);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Hubo un problema al actualizar la verificación en dos pasos.");
    }
}
