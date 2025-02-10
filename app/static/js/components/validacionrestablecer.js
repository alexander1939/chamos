document.addEventListener("DOMContentLoaded", function () {
    const nuevaContrasena = document.getElementById("nueva_contrasena");
    const confirmarContrasena = document.getElementById("confirmar_contrasena");
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

    nuevaContrasena.addEventListener("input", function () {
        validarContrasena();
        if (confirmarContrasena.value !== "") {
            validarCoincidencia();
        }
    });

    confirmarContrasena.addEventListener("input", validarCoincidencia);
});
