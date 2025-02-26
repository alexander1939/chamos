document.addEventListener("DOMContentLoaded", function () {
    const verificarBtn = document.querySelector("button[type='submit']");
    const MAX_INTENTOS = 3;
    const TIEMPO_BLOQUEO = 60 * 1000; // 1 minuto en milisegundos
    const emailInput = document.querySelector("input[name='email']");
    const email = emailInput ? emailInput.value : null; // Asegurar que haya un email disponible
    const storageKey = `intentos_${email}`;
    const bloqueoHastaInput = document.getElementById("bloqueo_hasta");

    function obtenerEstadoIntentos() {
        const datos = localStorage.getItem(storageKey);
        return datos ? JSON.parse(datos) : { intentos: 0, bloqueoHasta: null };
    }

    function guardarEstadoIntentos(intentos, bloqueoHasta) {
        localStorage.setItem(storageKey, JSON.stringify({ intentos, bloqueoHasta }));
    }

    function actualizarEstadoBoton() {
        const ahora = Date.now();
        let estado = obtenerEstadoIntentos();

        // Si `bloqueo_hasta` viene del backend, lo usamos como referencia
        let bloqueoDesdeServidor = bloqueoHastaInput ? parseInt(bloqueoHastaInput.value) * 1000 : null;

        // Determinar el tiempo de bloqueo final (el mayor entre cliente y servidor)
        let bloqueoFinal = Math.max(estado.bloqueoHasta || 0, bloqueoDesdeServidor || 0);

        if (bloqueoFinal && ahora < bloqueoFinal) {
            verificarBtn.disabled = true;
            const tiempoRestante = bloqueoFinal - ahora;
            console.log(`Botón deshabilitado por ${Math.ceil(tiempoRestante / 1000)} segundos`);
            setTimeout(habilitarBoton, tiempoRestante);
        } else {
            verificarBtn.disabled = false;
            guardarEstadoIntentos(0, null);
        }
    }

    function habilitarBoton() {
        verificarBtn.disabled = false;
        guardarEstadoIntentos(0, null);
        console.log("Botón habilitado nuevamente");
    }

    function registrarIntentoFallido() {
        let estado = obtenerEstadoIntentos();
        estado.intentos += 1;
        console.log(`Intento fallido ${estado.intentos}/${MAX_INTENTOS}`);

        if (estado.intentos >= MAX_INTENTOS) {
            estado.bloqueoHasta = Date.now() + TIEMPO_BLOQUEO;
            verificarBtn.disabled = true;
            console.log("Botón deshabilitado por 1 minuto");
            setTimeout(habilitarBoton, TIEMPO_BLOQUEO);
        }

        guardarEstadoIntentos(estado.intentos, estado.bloqueoHasta);
    }

    verificarBtn.addEventListener("click", function (event) {
        setTimeout(() => {
            const flashMessages = document.querySelectorAll(".alert");
            let bloqueoDetectado = false;

            flashMessages.forEach(msg => {
                if (msg.innerText.includes("Demasiados intentos fallidos")) {
                    bloqueoDetectado = true;
                }
            });

            if (bloqueoDetectado) {
                registrarIntentoFallido();
                actualizarEstadoBoton();
            }
        }, 500);  // Esperamos un poco más para capturar el mensaje flash
    });

    actualizarEstadoBoton();

    // Ocultar mensajes flash después de 5 segundos
    setTimeout(function () {
        document.querySelectorAll('.alert').forEach(msg => msg.style.display = 'none');
    }, 5000);
});
