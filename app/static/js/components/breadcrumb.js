let breadcrumbsCargado = false; // Control para evitar múltiples peticiones simultáneas

async function actualizarBreadcrumbs() {
    if (breadcrumbsCargado) return; // Si ya se está ejecutando, no lo vuelve a hacer
    breadcrumbsCargado = true; // Marca que se está ejecutando

    try {
        const breadcrumbsContainer = document.querySelector(".breadcrumbsx");
        if (!breadcrumbsContainer) return;

        const currentPath = window.location.pathname;
        const response = await fetch(`/api/breadcrumbs?path=${encodeURIComponent(currentPath)}`, {
            method: "GET",
            credentials: "include",
            headers: { "Content-Type": "application/json" }
        });

        if (!response.ok) {
            throw new Error("Error al obtener los breadcrumbs.");
        }

        const data = await response.json();
        breadcrumbsContainer.innerHTML = `
            <li class="breadcrumbsx-item">
                <a href="/">Home</a>
            </li>
        `;

        data.breadcrumbs.forEach(crumb => {
            breadcrumbsContainer.innerHTML += crumb.url
                ? `<li class="breadcrumbsx-item"><a href="${crumb.url}">${crumb.name}</a></li>`
                : `<li class="breadcrumbsx-item active">${crumb.name}</li>`;
        });

    } catch (error) {
        console.error("Error al actualizar breadcrumbs:", error);
    } finally {
        breadcrumbsCargado = false; // Permite que se pueda ejecutar nuevamente cuando cambie la ruta
    }
}
