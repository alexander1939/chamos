document.addEventListener("DOMContentLoaded", function () {
    let select = document.getElementById("category-select");
    let apiUrl = select.getAttribute("data-api-url");

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                console.error("Error al obtener categorías: Código", response.status);
                throw new Error("No autorizado");
            }
            return response.json();
        })
        .then(data => {
            console.log("Categorías obtenidas:", data);
            select.innerHTML = "";

            let optionTodos = document.createElement("option");
            optionTodos.value = "todos";
            optionTodos.textContent = "Todos";
            select.appendChild(optionTodos);

            if (Object.keys(data).length === 0) {
                select.innerHTML += '<option value="" disabled>No tienes acceso a ninguna categoría</option>';
            } else {
                for (let key in data) {
                    let option = document.createElement("option");
                    option.value = key;
                    option.textContent = data[key];
                    select.appendChild(option);
                }
            }
        })
        .catch(error => {
            console.error("Error al cargar categorías:", error);
            select.innerHTML = '<option value="" disabled>Error al cargar categorías</option>';
        });
});
