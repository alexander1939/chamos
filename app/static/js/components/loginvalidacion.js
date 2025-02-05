document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("loginForm"); // Cambié el id del formulario a 'loginForm'
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const submitButton = document.getElementById("submitButton");

    // Contenedores de error
    const emailError = document.getElementById("emailError");
    const passwordError = document.getElementById("passwordError");

    function validateInput(input, errorElement, regex, errorMessage) {
        input.addEventListener("input", function () {
            if (!regex.test(input.value.trim())) {
                errorElement.innerText = errorMessage;
            } else {
                errorElement.innerText = "";
            }
            checkFormValidity();
        });
    }

    function checkFormValidity() {
        submitButton.disabled = !(
            emailError.innerText === "" &&
            passwordError.innerText === ""
        );
    }

    // Validaciones en tiempo real
    validateInput(emailInput, emailError, /^[^\s@]+@[^\s@]+\.[^\s@]+$/, "El correo electrónico no es válido.");
    validateInput(passwordInput, passwordError, /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$/, "La contraseña debe tener al menos 8 caracteres, incluir una mayúscula, una minúscula y un número.");

    form.addEventListener("submit", function (event) {
        if (submitButton.disabled) {
            event.preventDefault();
        }
    });
});
