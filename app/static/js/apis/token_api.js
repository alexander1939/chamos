let previousToken = null;

async function hacerPeticionApi() {
    try {
        const response = await fetch('/api/validate_token', {
            method: 'GET',
            credentials: 'include'
        });

        if (response.status === 401 || response.status === 403) {
            console.warn('Token inválido, redirigiendo al login...');
            window.location.href = '/login';
        }else if (!response.ok) {
            console.error(`Error en la API (Código ${response.status}): ${response.statusText}`);
            return;
        }   
    } catch (error) {
        console.error('Error al validar el token:', error);
    }
}

function obtenerTokenActual() {
    // Obtener el token desde las cookies
    const name = 'token=';
    const decodedCookie = decodeURIComponent(document.cookie);
    const ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
            const token = c.substring(name.length, c.length);
            return token;
        }
    }
    return '';
}

function verificarCambioToken() {
    const currentToken = obtenerTokenActual();

    if (currentToken !== previousToken) {
        previousToken = currentToken;
        hacerPeticionApi();
    }
}

document.addEventListener("DOMContentLoaded", () => {
    setInterval(verificarCambioToken, 1000); // Verificar cada 1 segundo
});

document.addEventListener("click", hacerPeticionApi);
// document.addEventListener("keydown", hacerPeticionApi);
// document.addEventListener("mousemove", hacerPeticionApi);