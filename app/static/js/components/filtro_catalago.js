document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById('search-input');
    const cancelButton = document.getElementById('cancel-search');

    cancelButton.style.display = 'none';

    searchInput.addEventListener('input', debounce(function () {
        filterContent();
    }, 300));

    cancelButton.addEventListener('click', function () {
        cancelSearch();
    });
});

async function loadContent(query) {
    const modulo = window.location.pathname.split("/")[2];
    const tableBody = document.getElementById('content-container');
    const cancelButton = document.getElementById('cancel-search');

    try {
        const response = await fetch(`/buscar/${modulo}?query=${query}`, {
            method: 'GET',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            console.error(`Error en la API (Código ${response.status}): ${response.statusText}`);
            return;
        }

        const data = await response.json();
        tableBody.innerHTML = '';

        if (data.length === 0) {
            tableBody.innerHTML = `
                <div class="alert alert-info" role="alert">
                    No hay registros disponibles.
                </div>
            `;
        } else {
            data.forEach(item => {
                const row = document.createElement('div');
                row.classList.add('col', 'content-item');
                row.innerHTML = `
                    <div class="card shadow-sm border-light rounded">
                        <div class="card-body">
                            <h5 class="card-title">${item.nombre}</h5>
                            <p class="card-text">${item.descripcion}</p>
                            <div class="d-flex justify-content-between align-items-center">
                                <div>
                                    <a href="${item.detalles_url}" class="btn btn-primary btn-sm">Ver Detalles</a>
                                </div>
                                <div class="d-flex">
                                    ${item.can_edit ? `
                                        <a href="${item.edit_url}" class="btn btn-warning btn-sm me-2">
                                            <img src="${item.edit_image_url}" alt="Editar" width="20" height="20">
                                        </a>
                                    ` : ''}
                                    ${item.can_delete ? `
                                        <form action="${item.delete_url}" method="POST" style="display:inline-block;">
                                            <button type="submit" class="btn btn-danger btn-sm">
                                                <img src="${item.delete_image_url}" alt="Eliminar" width="20" height="20">
                                            </button>
                                        </form>
                                    ` : ''}
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                tableBody.appendChild(row);
            });
        }

        cancelButton.style.display = query.trim() !== '' ? 'inline-block' : 'none';

    } catch (error) {
        console.error('Error al obtener los contenidos:', error);
    }
}

function filterContent() {
    const searchInput = document.getElementById('search-input');
    const cancelButton = document.getElementById('cancel-search');
    const query = searchInput.value.trim();

    if (query !== "") {
        loadContent(query);
        cancelButton.style.display = "inline-block";
    } else {
        cancelSearch();
    }
}

function cancelSearch() {
    const searchInput = document.getElementById('search-input');
    const tableBody = document.getElementById('content-container');
    const cancelButton = document.getElementById('cancel-search');

    searchInput.value = '';
    tableBody.innerHTML = '';
    cancelButton.style.display = "none";

    loadContent('');
}

function debounce(func, delay) {
    let timeout;
    return function () {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, arguments), delay);
    };
}
