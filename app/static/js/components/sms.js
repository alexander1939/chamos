document.addEventListener("DOMContentLoaded", function () {
    const nuevaContrasena = document.getElementById("password");
    const confirmarContrasena = document.getElementById("confirm_password");
    const errorNuevaContrasena = document.getElementById("error-nueva-contrasena");
    const errorConfirmarContrasena = document.getElementById("error-contrasena");

    function validarContrasena() {
        const password = nuevaContrasena.value;
        const regex = /^(?=.*[A-Z])(?=.*\d).{8,}$/;

        if (password === "" || regex.test(password)) {
            errorNuevaContrasena.style.display = "none";
        } else {
            errorNuevaContrasena.style.display = "block";
        }
    }

    function validarCoincidencia() {
        if (confirmarContrasena.value === nuevaContrasena.value && nuevaContrasena.value !== "") {
            errorConfirmarContrasena.style.display = "none";
        } else {
            errorConfirmarContrasena.style.display = "block";
        }
    }

    // Validar contraseña al perder el foco o al escribir
    nuevaContrasena.addEventListener("blur", validarContrasena);
    nuevaContrasena.addEventListener("input", function () {
        if (nuevaContrasena.value !== "") {
            validarContrasena();
        }
    });

    // Validar coincidencia al perder el foco o al escribir
    confirmarContrasena.addEventListener("blur", validarCoincidencia);
    confirmarContrasena.addEventListener("input", function () {
        if (confirmarContrasena.value !== "") {
            validarCoincidencia();
        }
    });
});