document.getElementById("register-form").addEventListener("submit", async function (event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const errorDiv = document.getElementById("error-message");

    const response = await fetch(form.action, {
        method: "POST",
        body: formData,
        redirect: "follow"
    });

    if (response.redirected) {
        window.location.href = response.url;
    } else {
        const result = await response.json();
        errorDiv.textContent = result.error || "Ocurrió un error";
        errorDiv.style.display = "block";
    }
});

