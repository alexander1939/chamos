document.getElementById("loginForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const errorDiv = document.getElementById("error-message");

    try {
        const response = await fetch(form.action, {
            method: "POST",
            body: formData,
            redirect: "follow"
        });

        const result = await response.json();

        if (response.ok) {
            window.location.href = result.redirect_url;  // 🔹 Redirigir automáticamente al index
        } else {
            errorDiv.textContent = result.error || "Ocurrió un error al iniciar sesión.";
            errorDiv.style.display = "block";
        }
    } catch (error) {
        console.error("Error en la solicitud:", error);
        errorDiv.textContent = "Error inesperado. Inténtalo de nuevo.";
        errorDiv.style.display = "block";
    }
});
