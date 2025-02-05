from flask import Blueprint, jsonify
from app.middleware.menu_middleware import menu_required, get_privilege_content

menu = Blueprint('menu', __name__)

@menu.route('/api/menu', methods=['GET'])
@menu_required
def get_user_menu(user, privileges):
    """Devuelve los privilegios del usuario, incluyendo permisos `can_create` y `can_view`."""
    
    user_data = {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }

    data = get_privilege_content(user, privileges)

    return jsonify({"usuario": user_data, "privilegios": list(privileges.keys()), "contenido": data}), 200
