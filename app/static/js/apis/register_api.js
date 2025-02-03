document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('registerForm');
    const checkbox = document.getElementById('terms');
    const button = document.getElementById('submitButton');
    const errorMessagesDiv = document.getElementById('errorMessages');
    const errorTextSpan = document.getElementById('errorText');
    const successMessagesDiv = document.getElementById('successMessages');
    const successTextSpan = document.getElementById('successText');
    const termsErrorDiv = document.getElementById('termsError');

    // Habilitar o deshabilitar el botón según el checkbox de términos
    checkbox.addEventListener("change", function () {
        button.disabled = !checkbox.checked;
    });

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = {
            name: document.getElementById('name').value.trim(),
            phone: document.getElementById('phone').value.trim(),
            surnames: document.getElementById('surnames').value.trim(),
            email: document.getElementById('email').value.trim(),
            password: document.getElementById('password').value.trim()
        };

        if (!checkbox.checked) {
            termsErrorDiv.style.display = 'block';
            return;
        } else {
            termsErrorDiv.style.display = 'none';
        }

        fetch('/register/', {  // Asegúrate de que coincide con la URL de Flask
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData),
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    errorMessagesDiv.style.display = 'block';
                    errorTextSpan.textContent = data.error;
                    successMessagesDiv.style.display = 'none';
                } else {
                    successMessagesDiv.style.display = 'block';
                    successTextSpan.textContent = data.message;
                    errorMessagesDiv.style.display = 'none';

                    form.reset();
                    checkbox.checked = false;
                    button.disabled = true;

                    setTimeout(() => {
                        window.location.href = "/login";  // Redirigir al login después de registrar
                    }, 2000);
                }
            })
            .catch(() => {
                errorMessagesDiv.style.display = 'block';
                errorTextSpan.textContent = 'Hubo un error. Inténtalo de nuevo.';
            });
    });
});
