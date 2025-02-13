<<<<<<< HEAD
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("search-form");
    const select = document.getElementById("category-select");

    let categoriesLoaded = false;

    select.addEventListener("focus", function () {
        if (!categoriesLoaded) {
            loadCategories(select);
            categoriesLoaded = true;
        }
    });

    handleFormSubmit(form);
});

function debounce(func, delay) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
    };
}

function loadCategories(select) {
    const apiUrl = select.getAttribute("data-api-url");

    fetch(apiUrl)
        .then(response => handleFetchResponse(response, "Error al obtener categorías"))
        .then(data => populateCategories(select, data.categorias))
        .catch(error => handleFetchError(select, error));
}

function handleFormSubmit(form) {
    form.addEventListener("submit", debounce(function (event) {
        event.preventDefault();

        const { query, category } = getFormValues(form);
        if (!query.trim()) return;

        const searchUrl = buildSearchUrl(form, query, category);
        performSearch(searchUrl);
    }, 500));
}

function getFormValues(form) {
    const query = form.querySelector('input[name="query"]').value;
    const category = form.querySelector('select[name="category"]').value;
    return { query, category };
}

function buildSearchUrl(form, query, category) {
    const searchUrlBase = form.getAttribute("data-search-url");
    return `${searchUrlBase}?query=${encodeURIComponent(query)}&category=${encodeURIComponent(category)}`;
}

function performSearch(searchUrl) {
    fetch(searchUrl, {
        method: 'GET',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => handleFetchResponse(response, "Error en la búsqueda"))
        .then(data => displaySearchResults(data))
        .catch(error => console.error("Error al realizar la búsqueda:", error));
}

function handleFetchResponse(response, errorMessage) {
    if (!response.ok) {
        console.error(`${errorMessage}: Código ${response.status}`);
        throw new Error(errorMessage);
    }
    return response.json();
}

function handleFetchError(element, error) {
    console.error("Error:", error);
    element.innerHTML = '<option value="" disabled>Error al cargar categorías</option>';
}

function populateCategories(select, categorias) {
    select.innerHTML = "";

    const optionTodos = document.createElement("option");
    optionTodos.value = "todos";
    optionTodos.textContent = "Todos";
    select.appendChild(optionTodos);

    if (Object.keys(categorias).length === 0) {
        select.innerHTML += '<option value="" disabled>No tienes acceso a ninguna categoría</option>';
    } else {
        for (let key in categorias) {
            const option = document.createElement("option");
            option.value = key;
            option.textContent = categorias[key];
            select.appendChild(option);
        }
    }
}

function displaySearchResults(data) {
    console.log("Resultados de la búsqueda:", data);
}
=======
>>>>>>> b8496881b31cb2b37953143364eb31f749221f09
