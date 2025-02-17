/*
Código que se ejecuta al cargar el DOM:
1. Verifica si hay un ID de elemento. Si no, inicializa la eliminación.
2. Carga el catálogo del módulo actual.
3. Escucha cambios en la historia del navegador para recargar el catálogo.
*/
document.addEventListener("DOMContentLoaded", () => {
    const itemId = obtenerItemId();
    if (itemId) return;

    inicializarEliminacion();

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

/*
Inicializa la eliminación de elementos:
1. Escucha clics en botones con clase "btn-eliminar".
2. Muestra un cuadro de confirmación con SweetAlert2.
3. Si se confirma, elimina el elemento llamando a `eliminarElemento`.
*/
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

/*
Elimina un elemento enviando una solicitud DELETE al servidor:
1. Si la respuesta es exitosa, remueve el elemento del DOM.
2. Si hay un error, muestra un mensaje en consola y una alerta.
*/
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

        document.querySelector(`[data-id="${itemId}"]`).closest(".content-item").remove();

    } catch (error) {
        console.error("Error al eliminar:", error);
        alert("No se pudo eliminar el elemento.");
    }
}