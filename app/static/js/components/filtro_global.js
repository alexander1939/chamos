document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("global-search");
    const resultsContainer = document.getElementById("search-results");

    searchInput.addEventListener("input", function () {
        const query = searchInput.value.trim();
        if (query.length < 2) {
            resultsContainer.style.display = "none";
            return;
        }

        fetch(`/buscar?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                resultsContainer.innerHTML = "";
                if (data.length === 0) {
                    resultsContainer.innerHTML = "<div>No se encontraron resultados</div>";
                } else {
                    data.forEach(item => {
                        const div = document.createElement("div");
                        div.innerHTML = `<strong>${item.tipo}:</strong> ${item.titulo} <br> ${item.descripcion}`;
                        div.onclick = () => {
                            if (item.tipo === "Usuario") {
                                window.location.href = `/perfil/${item.id}`;
                            } else {
                                window.location.href = `/${item.tipo.toLowerCase()}/${item.id}`;
                            }
                        };
                        resultsContainer.appendChild(div);
                    });
                }
                resultsContainer.style.display = "block";
            })
            .catch(error => console.error("Error en la búsqueda:", error));
    });

    // Ocultar resultados si se hace clic fuera
    document.addEventListener("click", function (e) {
        if (!searchInput.contains(e.target) && !resultsContainer.contains(e.target)) {
            resultsContainer.style.display = "none";
        }
    });
});