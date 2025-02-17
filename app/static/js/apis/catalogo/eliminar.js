document.addEventListener("DOMContentLoaded", () => {
    const itemId = obtenerItemId();
    if (itemId) return;

    inicializarEliminacion(); // 🔹 Se inicializa la eliminación dinámica

    const modulo = obtenerModulo();
    if (modulo) {
        cargarCatalogo(modulo);
    }

    window.addEventListener("popstate", () => {
        const modulo = obtenerModulo();
        if (modulo) {
            cargarCatalogo(modulo);
        }
    });
});

// 🔹 Función para inicializar los eventos de eliminación
function inicializarEliminacion() {
    document.body.addEventListener("click", async (e) => {
        const botonEliminar = e.target.closest(".btn-eliminar");
        if (botonEliminar) {
            e.preventDefault();

            const modulo = botonEliminar.getAttribute("data-modulo");
            const itemId = botonEliminar.getAttribute("data-id");

            Swal.fire({
                title: "¿Estás seguro?",
                text: "No podrás revertir esta acción",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#d33",
                cancelButtonColor: "#3085d6",
                confirmButtonText: "Sí, eliminar",
                cancelButtonText: "Cancelar"
            }).then(async (result) => {
                if (result.isConfirmed) {
                    await eliminarElemento(modulo, itemId);
                    Swal.fire("¡Eliminado!", "El elemento ha sido eliminado.", "success");
                }
            });
        }
    });
}


// 🔹 Función para eliminar un elemento sin recargar la página
async function eliminarElemento(modulo, itemId) {
    try {
        const response = await fetch(`/api/catalogo/delete/?modulo=${modulo}`, {
            method: "DELETE",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id: itemId })
        });


        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        // Eliminar visualmente el elemento del DOM sin recargar la página
        document.querySelector(`[data-id="${itemId}"]`).closest(".content-item").remove();

    } catch (error) {
        console.error("Error al eliminar:", error);
        alert("No se pudo eliminar el elemento.");
    }
}

