from flask import request
import requests

BREADCRUMB_NAMES = {
    "/error-404": "Página no encontrada"
}

def generate_breadcrumbs():
    """
    Genera breadcrumbs dinámicos para rutas que incluyen "detalle" o "editar" usando la API.
    """
    path_segments = [seg for seg in request.path.strip("/").split("/") if seg]
    breadcrumbs = []
    accumulated_path = ""

    for i, segment in enumerate(path_segments):
        accumulated_path += f"/{segment}"

        # Evitar que "catalogo" aparezca en la visualización, pero mantener su estructura en la URL
        if segment.lower() == "catalogo":
            continue

        if segment in ["detalle", "editar"] and i + 1 < len(path_segments):
            parent_segment = path_segments[i - 1] if i > 0 else None
            item_id = path_segments[i + 1]  # Tomamos el item_id de la URL

            if parent_segment:
                # Llamada a la API para obtener el detalle del ítem, similar a la lógica de mostrar_detalle
                api_url = f"http://localhost:5000/api/catalogo/detalle/?modulo={parent_segment}"
                response = requests.get(api_url, json={'id': item_id}, cookies=request.cookies)

                if response.status_code == 200:
                    response_json = response.json()
                    can_view = response_json.get("can_view", False)
                    if can_view:
                        item = response_json.get("detalle", {})
                        if item:
                            # Mostrar el nombre del item en el breadcrumb
                            name = f"Detalles {item.get('nombre')}" if segment == "detalle" else f"Editar {item.get('nombre')}"
                        else:
                            name = f"{segment.capitalize()} no encontrado"
                    else:
                        name = f"No tienes acceso para ver este {parent_segment.capitalize()}"
                else:
                    # Si la API devuelve un error, se muestra el mensaje adecuado
                    name = f"{segment.capitalize()} no encontrado"

            else:
                name = f"{segment.capitalize()} no definido"

            breadcrumbs.append({
                "name": name,
                "url": None  
            })
            break 

        else:
            name = BREADCRUMB_NAMES.get(accumulated_path, segment.capitalize())
            url = accumulated_path if i != len(path_segments) - 1 else None

            breadcrumbs.append({
                "name": name,
                "url": url  
            })

    return breadcrumbs
