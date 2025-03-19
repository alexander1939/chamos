/* 
document.addEventListener("DOMContentLoaded", async () => {
    const tableBody = document.querySelector("tbody");
    
    let usersData = [];

    try {
        const response = await fetch("/api/users/", {
            method: "GET",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
        });

        if (!response.ok) {
            console.error(`Error en la API (Código ${response.status}): ${response.statusText}`);
            return;
        }

        usersData = await response.json();
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
});

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
                <div class="privilege-options">
                    <label><input type="checkbox" class="can-create" ${privilege?.can_create ? "checked" : ""} ${hasPrivilege ? "" : "disabled"}> Crear</label>
                    <label><input type="checkbox" class="can-edit" ${privilege?.can_edit ? "checked" : ""} ${hasPrivilege ? "" : "disabled"}> Editar</label>
                    <label><input type="checkbox" class="can-delete" ${privilege?.can_delete ? "checked" : ""} ${hasPrivilege ? "" : "disabled"}> Eliminar</label>
                    <label><input type="checkbox" class="can-view" ${privilege?.can_view ? "checked" : ""} ${hasPrivilege ? "" : "disabled"}> Consultar</label>
                </div>
            </td>
        `;
    });

    return cells;
}

document.addEventListener("change", async (event) => {
    if (event.target.classList.contains("privilege-toggle")) {
        const privilegeContainer = event.target.closest("td").querySelector(".privilege-options");
        const checkboxes = privilegeContainer.querySelectorAll("input[type='checkbox']");
        checkboxes.forEach(cb => cb.disabled = !event.target.checked);
    }
    
    if (event.target.classList.contains("privilege-toggle") || event.target.classList.contains("can-create") || event.target.classList.contains("can-edit") || event.target.classList.contains("can-delete") || event.target.classList.contains("can-view")) {
        const row = event.target.closest("tr");
        const userId = row.getAttribute("data-user-id");
        const updatedPrivileges = [];

        row.querySelectorAll(".privilege-toggle").forEach(privilegeCheckbox => {
            const privilegeName = privilegeCheckbox.getAttribute("data-privilege");
            const privilegeOptions = privilegeCheckbox.closest("td").querySelector(".privilege-options");

            if (privilegeCheckbox.checked) {
                updatedPrivileges.push({
                    id: getPrivilegeIdByName(privilegeName),
                    can_create: privilegeOptions.querySelector(".can-create").checked,
                    can_edit: privilegeOptions.querySelector(".can-edit").checked,
                    can_delete: privilegeOptions.querySelector(".can-delete").checked,
                    can_view: privilegeOptions.querySelector(".can-view").checked
                });
            }
        });

        await updateUserPrivileges(userId, updatedPrivileges);
    }
});

function getPrivilegeIdByName(privilegeName) {
    const privilegeMap = {
        "Materias": 1,
        "Proyectos": 3,
        "Juegos": 2
    };
    return privilegeMap[privilegeName] || null;
}

async function updateUserPrivileges(userId, privileges) {
    try {
        const response = await fetch(`/api/users/${userId}/privileges`, {
            method: "PUT",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ privileges })
        });

        const result = await response.json();

        if (response.ok) {
            Swal.fire({
                icon: "success",
                title: "Éxito",
                text: result.message,
                confirmButtonText: "Aceptar"
            });
        } else {
            console.error("Error al actualizar:", result.error);
            Swal.fire({
                icon: "error",
                title: "Error",
                text: "Error al actualizar privilegios.",
                confirmButtonText: "Aceptar"
            });
        }
    } catch (error) {
        console.error("Error al conectar con la API:", error);
        Swal.fire({
            icon: "error",
            title: "Error",
            text: "No se pudo actualizar los privilegios.",
            confirmButtonText: "Aceptar"
        });
    }
}

*/