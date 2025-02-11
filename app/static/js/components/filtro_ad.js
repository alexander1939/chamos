document.addEventListener("DOMContentLoaded", () => {
    fetchAndRenderUsers('');

    const searchInput = document.getElementById('search-input');
    searchInput.addEventListener('input', debounce(function () {
        filterContent(searchInput.value);
    }, 300));
});

async function fetchAndRenderUsers(query = '') {
    const tableBody = document.getElementById("user-table-body");

    try {
        const response = await fetch(`/buscar/privilegios?query=${query}`, {
            method: "GET",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
        });

        if (!response.ok) {
            console.error(`Error en la API (Código ${response.status}): ${response.statusText}`);
            return;
        }

        const usersData = await response.json();
        if (!Array.isArray(usersData)) {
            console.error("La API no devolvió una lista de usuarios:", usersData);
            return;
        }

        tableBody.innerHTML = "";

        usersData.forEach(user => {
            let row = `<tr data-user-id="${user.id}">
            <td>${user.name} ${user.surnames}</td>
            ${generatePrivilegesCells(user)}
        </tr>`;
            tableBody.innerHTML += row;
        });

    } catch (error) {
        console.error("Error al conectar con la API:", error);
    }
}

function generatePrivilegesCells(user) {
    const privilegeNames = ["Materias", "Proyectos", "Juegos"];
    let cells = "";

    privilegeNames.forEach(privName => {
        let privilege = user.privileges.find(p => p.name === privName);
        let hasPrivilege = privilege !== undefined;

        cells += `
        <td>
            <label>
                <input type="checkbox" class="privilege-toggle" data-privilege="${privName}" ${hasPrivilege ? "checked" : ""}> ${privName}
            </label>
            <div class="privilege-options" style="display: ${hasPrivilege ? "block" : "none"};">
                <label><input type="checkbox" class="can-create" ${privilege?.can_create ? "checked" : ""}> Crear</label>
                <label><input type="checkbox" class="can-edit" ${privilege?.can_edit ? "checked" : ""}> Editar</label>
                <label><input type="checkbox" class="can-delete" ${privilege?.can_delete ? "checked" : ""}> Eliminar</label>
                <label><input type="checkbox" class="can-view" ${privilege?.can_view ? "checked" : ""}> Consultar</label>
            </div>
        </td>
        `;
    });

    return cells;
}

function filterContent(query) {
    fetchAndRenderUsers(query);

    let cancelButton = document.getElementById('cancel-search');
    if (query.trim() !== '') {
        cancelButton.style.display = 'inline';
    } else {
        cancelButton.style.display = 'none';
    }
}

function cancelSearch() {
    document.getElementById('search-input').value = '';
    fetchAndRenderUsers('');
}
function debounce(func, delay) {
    let timeout;
    return function () {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, arguments), delay);
    };
}