document.addEventListener('DOMContentLoaded', function () {
    const breadcrumbCurrent = document.getElementById('current-breadcrumb'); // Elemento del breadcrumb
    const breadcrumbList = document.querySelector('.breadcrumbs__list'); // Lista del breadcrumb

    // Función para actualizar el breadcrumb dinámicamente
    function updateBreadcrumb(currentPage) {
        // Limpia el breadcrumb actual
        breadcrumbList.innerHTML = `
            <li class="breadcrumbs__item">
                <a href="mi_nombre.html" class="breadcrumbs__link">Home</a>
            </li>
            <li class="breadcrumbs__item">
                <span class="breadcrumbs__separator">/</span>
            </li>
            <li class="breadcrumbs__item">
                <span class="breadcrumbs__current" id="current-breadcrumb">${currentPage}</span>
            </li>
        `;
    }

    // Detecta en qué página estás
    const currentPath = window.location.pathname;

    if (currentPath.includes('materias.html')) {
        updateBreadcrumb('Materias');
    } else if (currentPath.includes('matematicas.html')) {
        updateBreadcrumb('Matemáticas');
    } else if (currentPath.includes('ingles.html')) {
        updateBreadcrumb('Inglés');
    } else if (currentPath.includes('ciencias.html')) {
        updateBreadcrumb('Ciencias');
    } else {
        updateBreadcrumb('Home');
    }
});
