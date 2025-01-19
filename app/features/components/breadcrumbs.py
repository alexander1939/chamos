from flask import request


BREADCRUMB_NAMES = {
    #solo ponle un nombre si es nesesario a los BREADCRUMB, si no tomara el nombre de las rutas
    #ejemplo:  "/tavo/juegos": "Juegos de Tavo"

    "/error-404": "Página no encontrada"
}

def generate_breadcrumbs():

    path_segments = [seg for seg in request.path.strip("/").split("/") if seg]
    breadcrumbs = []

    accumulated_path = ""
    for segment in path_segments:
        accumulated_path += f"/{segment}"
        name = BREADCRUMB_NAMES.get(accumulated_path, segment.capitalize())
        breadcrumbs.append({
            "name": name,
            "url": accumulated_path if segment != path_segments[-1] else None
        })


    return breadcrumbs
