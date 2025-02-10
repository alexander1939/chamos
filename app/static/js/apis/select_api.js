document.addEventListener("DOMContentLoaded", function () {
    let select = document.getElementById("category-select");
    let apiUrl = select.getAttribute("data-api-url");
    fetch(apiUrl)
        .then(response => {
            if (!response.ok) throw new Error("No autorizado");
            return response.json();
        })
        .then(data => {
            select.innerHTML = "";
            if (Object.keys(data).length === 0) {
                select.innerHTML = '<option value="" disabled>No tienes acceso a ninguna categoría</option>';
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
