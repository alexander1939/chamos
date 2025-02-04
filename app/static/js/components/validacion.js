document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("registerForm");
    const nameInput = document.getElementById("name");
    const surnameInput = document.getElementById("surnames");
    const phoneInput = document.getElementById("phone");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const termsCheckbox = document.getElementById("terms");
    const submitButton = document.getElementById("submitButton");

    // Contenedores de error
    const nameError = document.getElementById("nameError");
    const surnamesError = document.getElementById("surnamesError");
    const phoneError = document.getElementById("phoneError");
    const emailError = document.getElementById("emailError");
    const passwordError = document.getElementById("passwordError");

    function validateForm() {
        let isValid = true;

        // Validar nombre
        const nameRegex = /^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]+$/;
        if (!nameRegex.test(nameInput.value.trim()) || nameInput.value.trim().length < 4) {
            nameError.innerText = "El nombre debe contener solo letras y tener al menos 4 caracteres.";
            isValid = false;
        } else {
            nameError.innerText = "";
        }

        // Validar apellidos
        if (!nameRegex.test(surnameInput.value.trim()) || surnameInput.value.trim().length < 4) {
            surnamesError.innerText = "Los apellidos deben contener solo letras y tener al menos 4 caracteres.";
            isValid = false;
        } else {
            surnamesError.innerText = "";
        }

        // Validar teléfono (exactamente 10 dígitos)
        const phoneRegex = /^\d{10}$/;
        if (!phoneRegex.test(phoneInput.value.trim())) {
            phoneError.innerText = "El teléfono debe tener exactamente 10 dígitos.";
            isValid = false;
        } else {
            phoneError.innerText = "";
        }

        // Validar correo electrónico
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailInput.value.trim())) {
            emailError.innerText = "El correo electrónico no es válido.";
            isValid = false;
        } else {
            emailError.innerText = "";
        }

        // Validar contraseña (mínimo 8 caracteres, 1 mayúscula, 1 minúscula, 1 número)
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$/;
        if (!passwordRegex.test(passwordInput.value.trim())) {
            passwordError.innerText = "La contraseña debe tener al menos 8 caracteres, incluir una mayúscula, una minúscula y un número.";
            isValid = false;
        } else {
            passwordError.innerText = "";
        }

        return isValid;
    }

    // Mostrar los mensajes de error desde el inicio
    validateForm();

    // Habilitar/deshabilitar el botón de envío
    form.addEventListener("input", function () {
        submitButton.disabled = !validateForm();
    });

    form.addEventListener("submit", function (event) {
        if (!validateForm()) {
            event.preventDefault();
        }
    });

    // Validación en tiempo real del teléfono (solo números)
    phoneInput.addEventListener("input", function () {
        this.value = this.value.replace(/\D/g, ""); // Eliminar caracteres no numéricos
        if (this.value.length > 10) {
            this.value = this.value.slice(0, 10); // Limitar a 10 caracteres
        }
    });

    // Validación en tiempo real para nombre y apellidos (solo letras y espacios)
    function restrictToLetters(input) {
        input.addEventListener("input", function () {
            this.value = this.value.replace(/[^a-zA-ZÁÉÍÓÚáéíóúÑñ\s]/g, ""); // Eliminar números y caracteres especiales
        });
    }

    restrictToLetters(nameInput);
    restrictToLetters(surnameInput);
});
