// Función para normalizar textos (eliminar acentos y convertir a minúsculas)
function normalizarTexto(texto) {
    return texto
        .normalize('NFD')  // Separa los caracteres y sus acentos
        .replace(/[\u0300-\u036f]/g, '')  // Elimina los acentos
        .toLowerCase();  // Convierte a minúsculas
}

// Función para filtrar usuarios
function filtrarUsuarios() {
    const input = normalizarTexto(document.getElementById('search-input').value);
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        const name = normalizarTexto(card.getAttribute('data-name'));
        const email = normalizarTexto(card.getAttribute('data-email'));
        const phone = normalizarTexto(card.getAttribute('data-phone'));

        if (name.includes(input) || email.includes(input) || phone.includes(input)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Asignar el evento de búsqueda al input
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', filtrarUsuarios);
    }
});