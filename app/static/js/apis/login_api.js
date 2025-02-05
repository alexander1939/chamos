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

        fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData),
            credentials: 'include'
        })
            .then(response => response.json().then(data => ({ status: response.status, body: data })))
            .then(({ status, body }) => {
                if (status !== 200) {
                    throw new Error(body.error || "Error al iniciar sesión");
                }

                successMessagesDiv.style.display = 'block';
                successTextSpan.textContent = body.message;
                errorMessagesDiv.style.display = 'none';



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

function verificarSesion() {
    fetch('/api/protected/', { method: 'GET', credentials: 'include' })
        .then(response => {
            if (response.status === 401) {
                console.log("Token expirado, intentando renovar...");

                return fetch('/api/refresh/', { method: 'POST', credentials: 'include' })
                    .then(res => res.json())
                    .then(data => {
                        if (data.token) {
                            console.log("Token renovado con éxito");
                        } else {
                            window.location.href = "/login";
                        }
                    });
            }
        })
        .catch(() => window.location.href = "/login");
}

verificarSesion();
