document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('loginForm');
    const errorMessagesDiv = document.getElementById('errorMessages');
    const errorTextSpan = document.getElementById('errorText');
    const successMessagesDiv = document.getElementById('successMessages');
    const successTextSpan = document.getElementById('successText');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = {
            email: document.getElementById('email').value.trim(),
            password: document.getElementById('password').value.trim()
        };

        fetch('/login/', {  // Asegúrate de que la URL coincide con la ruta en Flask
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData),
        })
            .then(response => response.json()
                .then(data => ({ status: response.status, body: data })))
            .then(({ status, body }) => {
                if (status !== 200) {
                    throw new Error(body.error || "Error al iniciar sesión");
                }

                successMessagesDiv.style.display = 'block';
                successTextSpan.textContent = body.message;
                errorMessagesDiv.style.display = 'none';

                // Guardar el token en localStorage
                localStorage.setItem("token", `Bearer ${body.token}`);

                setTimeout(() => {
                    window.location.href = "/";
                }, 2000);
            })
            .catch(error => {
                errorMessagesDiv.style.display = 'block';
                errorTextSpan.textContent = error.message;
            });
    });
});
