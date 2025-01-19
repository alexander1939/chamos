from flask import request


BREADCRUMB_NAMES = {
    """" 
         Aquí guardamos nombres personalizados para algunas rutas.
         solo ponle un nombre si es nesesario a los BREADCRUMB, si no tomara el nombre de las rutas 
         ejemplo:  "/tavo/juegos": "Juegos de Tavo"

    """

    "/error-404": "Página no encontrada"
}

def generate_breadcrumbs():

    """
    Esta función genera los 'breadcrumbs'.
    Se basa en la URL de la solicitud (request.path) para crear los elementos de la ruta.
    
    1. Divide la ruta en segmentos.
    2. Crea una lista de diccionarios con 'nombre' y 'url' para cada segmento.
    3. El nombre se obtiene de un diccionario predefinido (BREADCRUMB_NAMES) o del nombre del segmento en sí (De las rutas).
    4. La URL es la ruta acumulada hasta el momento.

    regresa algo asi: [ {"name": "Tavo", "url": "/tavo"} ]
    """

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
