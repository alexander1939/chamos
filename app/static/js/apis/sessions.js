document.addEventListener("DOMContentLoaded", () => {
    const deleteButtons = document.querySelectorAll(".delete-session");

    deleteButtons.forEach(button => {
        button.addEventListener("click", async (event) => {
            const sessionId = event.target.getAttribute("data-session-id");
            await deleteSession(sessionId);
        });
    });
});

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
