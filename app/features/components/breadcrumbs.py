from flask import request
from flask_login import current_user
from app.features.materia.model import Materia
from app.features.auth.model import User
from app.features.juegos.model import Juegos
from app.features.proyectos.model import Proyectos



BREADCRUMB_NAMES = {
    "/error-404": "Página no encontrada"
}

def generate_breadcrumbs():
    """
    Genera breadcrumbs dinámicos para rutas que incluyen "detalle" o "editar".
    """
    MODELS_MAP = {
        "materias": Materia,
        "juegos":Juegos,
        "proyectos": Proyectos
    }

    path_segments = [seg for seg in request.path.strip("/").split("/") if seg]
    breadcrumbs = []
    accumulated_path = ""

    for i, segment in enumerate(path_segments):
        accumulated_path += f"/{segment}"

        if segment in ["detalles", "editar"] and i + 1 < len(path_segments):
            parent_segment = path_segments[i - 1] if i > 0 else None
            item_id = path_segments[i + 1]  

            model = MODELS_MAP.get(parent_segment)
            if model:
                item = model.query.get(item_id)
                if item:
                    if current_user.is_authenticated and current_user.role == "Admin":
                        user = User.query.get(item.id_usuario)  
                        if user:
                            # Insertamos el breadcrumb del usuario en la posición 1 (después de "Home")
                            breadcrumbs.insert(0, {
                                "name": user.name,  
                                "url": None  
                            })
                    
                    if segment == "detalles":
                        name = f"Detalle de {item.nombre}"
                    elif segment == "editar":
                        name = f"Editar {item.nombre}"
                else:
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

            if current_user.is_authenticated and current_user.role == "Admin":
                breadcrumbs.append({
                    "name": name,
                    "url": None  
                })
            else:
                breadcrumbs.append({
                    "name": name,
                    "url": url  
                })

    return breadcrumbs
