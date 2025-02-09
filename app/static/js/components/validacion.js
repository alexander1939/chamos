document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("registerForm");
    const nameInput = document.getElementById("name");
    const surnameInput = document.getElementById("surnames");
    const phoneInput = document.getElementById("phone");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const termsCheckbox = document.getElementById("terms");
    const submitButton = document.getElementById("submitButton");

    const nameError = document.getElementById("nameError");
    const surnamesError = document.getElementById("surnamesError");
    const phoneError = document.getElementById("phoneError");
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
        const allFieldsValid =
            nameError.innerText === "" &&
            surnamesError.innerText === "" &&
            phoneError.innerText === "" &&
            emailError.innerText === "" &&
            passwordError.innerText === "";

        submitButton.disabled = !(allFieldsValid && termsCheckbox.checked);
    }

    validateInput(nameInput, nameError, /^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]{4,}$/, "El nombre debe contener solo letras y tener al menos 4 caracteres.");
    validateInput(surnameInput, surnamesError, /^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]{4,}$/, "Los apellidos deben contener solo letras y tener al menos 4 caracteres.");
    validateInput(phoneInput, phoneError, /^\d{10}$/, "El teléfono debe tener exactamente 10 dígitos.");
    validateInput(emailInput, emailError, /^[^\s@]+@[^\s@]+\.[^\s@]+$/, "El correo electrónico no es válido.");
    validateInput(passwordInput, passwordError, /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$/, "La contraseña debe tener al menos 8 caracteres, incluir una mayúscula, una minúscula y un número.");

    phoneInput.addEventListener("input", function () {
        this.value = this.value.replace(/\D/g, "").slice(0, 10);
        if (this.value.length === 10) {
            phoneError.innerText = "";
        }
    });

    function restrictToLetters(input) {
        input.addEventListener("input", function () {
            this.value = this.value.replace(/[^a-zA-ZÁÉÍÓÚáéíóúÑñ\s]/g, "");
        });
    }

    restrictToLetters(nameInput);
    restrictToLetters(surnameInput);

    termsCheckbox.addEventListener("change", checkFormValidity);

    form.addEventListener("submit", function (event) {
        if (submitButton.disabled) {
            event.preventDefault();
        }
    });
});
