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
    const pregunta1Error = document.getElementById("pregunta1Error");
    const pregunta2Error = document.getElementById("pregunta2Error");
    const respuesta1Error = document.getElementById("respuesta1Error");
    const respuesta2Error = document.getElementById("respuesta2Error");

    // Función para validar los campos
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

    // Función para validar select (preguntas)
    function validateSelect(select, errorElement, errorMessage) {
        select.addEventListener("change", function () {
            if (select.value === "") {
                errorElement.innerText = errorMessage;
            } else {
                errorElement.innerText = "";
            }
            checkFormValidity();
        });
    }

    // Función para validar respuestas
    function validateResponse(input, errorElement) {
        input.addEventListener("input", function () {
            // Eliminar espacios al inicio y al final
            const trimmedValue = input.value.trim();
            input.value = trimmedValue;

            if (trimmedValue.length < 2) {
                errorElement.innerText = "La respuesta debe tener al menos 2 caracteres.";
            } else {
                errorElement.innerText = "";
            }
            checkFormValidity();
        });
    }

    // Función para chequear si el formulario es válido
    function checkFormValidity() {
        const allFieldsValid =
            nameError.innerText === "" &&
            surnamesError.innerText === "" &&
            phoneError.innerText === "" &&
            emailError.innerText === "" &&
            passwordError.innerText === "" &&
            pregunta1Error.innerText === "" &&
            pregunta2Error.innerText === "" &&
            respuesta1Error.innerText === "" &&
            respuesta2Error.innerText === "";

        submitButton.disabled = !(allFieldsValid && termsCheckbox.checked);
    }

    // Validaciones para campos de texto
    validateInput(nameInput, nameError, /^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]{4,}$/, "El nombre debe contener solo letras y tener al menos 4 caracteres.");
    validateInput(surnameInput, surnamesError, /^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]{4,}$/, "Los apellidos deben contener solo letras y tener al menos 4 caracteres.");
    validateInput(phoneInput, phoneError, /^\d{10}$/, "El teléfono debe tener exactamente 10 dígitos.");
    validateInput(emailInput, emailError, /^[^\s@]+@[^\s@]+\.[^\s@]+$/, "El correo electrónico no es válido.");
    validateInput(passwordInput, passwordError, /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$/, "La contraseña debe tener al menos 8 caracteres, incluir una mayúscula, una minúscula y un número.");

    // Validaciones para los select y respuestas
    const pregunta1Select = document.getElementById("pregunta1");
    const pregunta2Select = document.getElementById("pregunta2");
    const respuesta1Input = document.getElementById("respuesta1");
    const respuesta2Input = document.getElementById("respuesta2");

    validateSelect(pregunta1Select, pregunta1Error, "Debes seleccionar una opción.");
    validateSelect(pregunta2Select, pregunta2Error, "Debes seleccionar una opción.");
    validateResponse(respuesta1Input, respuesta1Error);
    validateResponse(respuesta2Input, respuesta2Error);

    // Validación de teléfono (solo números)
    phoneInput.addEventListener("input", function () {
        this.value = this.value.replace(/\D/g, "").slice(0, 10);
        if (this.value.length === 10) {
            phoneError.innerText = "";
        }
    });

    // Restringir caracteres a solo letras para nombre y apellidos
    function restrictToLetters(input) {
        input.addEventListener("input", function () {
            this.value = this.value.replace(/[^a-zA-ZÁÉÍÓÚáéíóúÑñ\s]/g, "");
        });
    }

    restrictToLetters(nameInput);
    restrictToLetters(surnameInput);

    // Verificar que los términos sean aceptados
    termsCheckbox.addEventListener("change", checkFormValidity);

    // Prevenir envío del formulario si no es válido
    form.addEventListener("submit", function (event) {
        if (submitButton.disabled) {
            event.preventDefault();
        }
    });
});
