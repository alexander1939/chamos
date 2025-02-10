document.addEventListener("DOMContentLoaded", function () {
    console.log("Script de validación cargado");

    function validarEmail(input, errorElement) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!regex.test(input.value.trim())) {
            errorElement.innerText = "Por favor, introduce un correo válido.";
            input.classList.add("is-invalid");
            return false;
        } else {
            errorElement.innerText = "";
            input.classList.remove("is-invalid");
            return true;
        }
    }

    function validarPassword(input, errorElement) {
        if (input.value.trim().length < 6) {
            errorElement.innerText = "La contraseña debe tener al menos 8 caracteres.";
            input.classList.add("is-invalid");
            return false;
        } else {
            errorElement.innerText = "";
            input.classList.remove("is-invalid");
            return true;
        }
    }

    function agregarValidacion(formulario) {
        const emailInput = formulario.querySelector("input[name='email']");
        const passwordInput = formulario.querySelector("input[name='password']");
        const emailError = formulario.querySelector("#email-error") || document.createElement("div");
        const passwordError = formulario.querySelector("#password-error") || document.createElement("div");

        emailError.classList.add("invalid-feedback");
        passwordError.classList.add("invalid-feedback");

        if (!formulario.querySelector("#email-error")) {
            emailInput.insertAdjacentElement("afterend", emailError);
        }
        if (passwordInput && !formulario.querySelector("#password-error")) {
            passwordInput.insertAdjacentElement("afterend", passwordError);
        }

        formulario.addEventListener("submit", function (event) {
            let emailValido = validarEmail(emailInput, emailError);
            let passwordValido = passwordInput ? validarPassword(passwordInput, passwordError) : true;

            if (!emailValido || !passwordValido) {
                event.preventDefault();
            }
        });

        emailInput.addEventListener("input", () => validarEmail(emailInput, emailError));
        if (passwordInput) {
            passwordInput.addEventListener("input", () => validarPassword(passwordInput, passwordError));
        }
    }

    // Aplicar validación a ambos formularios si existen
    const loginForm = document.getElementById("loginForm");
    const recuperarForm = document.getElementById("recuperar-form");

    if (loginForm) {
        console.log("Validación aplicada al formulario de login");
        agregarValidacion(loginForm);
    }
    if (recuperarForm) {
        console.log("Validación aplicada al formulario de recuperación de contraseña");
        agregarValidacion(recuperarForm);
    }
});
