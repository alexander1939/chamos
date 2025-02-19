from flask import Blueprint, jsonify, request
import requests

BREADCRUMB_NAMES = {
    "/error-404": "Página no encontrada"
}

breadcrumbs_bp = Blueprint('breadcrumbs', __name__)

def generate_breadcrumbs(path):
    """
    Genera breadcrumbs dinámicos para la ruta proporcionada.
    """
    path_segments = [seg for seg in path.strip("/").split("/") if seg]
    breadcrumbs = []
    accumulated_path = ""

    if len(path_segments) >= 4 and path_segments[2] in ["detalle", "editar"]:
        modulo = path_segments[1]  
        action = path_segments[2] 
        item_id = path_segments[3]  

        api_url = f"http://localhost:5000/api/catalogo/detalle/?modulo={modulo}&id={item_id}"
        response = requests.get(api_url, cookies=request.cookies)

        if response.status_code == 200:
            response_json = response.json()
            item = response_json.get("detalle", {})
            item_name = item.get("nombre", f"ID {item_id}") 

            breadcrumbs.append({"name": modulo.capitalize(), "url": f"/catalogo/{modulo}/"})
            breadcrumbs.append({"name": f"{action.capitalize()} {item_name}", "url": None})  
        else:
            breadcrumbs.append({"name": modulo.capitalize(), "url": f"/catalogo/{modulo}/"})
            breadcrumbs.append({"name": f"{action.capitalize()} no encontrado", "url": None}) 
        return breadcrumbs

    if len(path_segments) >= 3 and path_segments[1] == "agregar":
        modulo = path_segments[2] 
        action = path_segments[1]  

        breadcrumbs.append({"name": modulo.capitalize(), "url": f"/catalogo/{modulo}/"})
        breadcrumbs.append({"name": action.capitalize(), "url": None})  
        return breadcrumbs

    for i, segment in enumerate(path_segments):
        accumulated_path += f"/{segment}"

        if segment.lower() == "catalogo":
            continue  

        name = BREADCRUMB_NAMES.get(accumulated_path, segment.capitalize())
        url = accumulated_path if i != len(path_segments) - 1 else None

        breadcrumbs.append({"name": name, "url": url})

    return breadcrumbs

@breadcrumbs_bp.route("/api/breadcrumbs", methods=["GET"])
def get_breadcrumbs():
    path = request.args.get("path", "/")  
    breadcrumbs = generate_breadcrumbs(path)
    return jsonify({"breadcrumbs": breadcrumbs})
