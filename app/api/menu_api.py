from flask import Blueprint, jsonify
from app.middleware.menu_middleware import menu_required, get_privilege_content

menu = Blueprint('menu', __name__)

@menu.route('/api/menu', methods=['GET'])
@menu_required
def get_user_menu(user, privileges):
    """Devuelve los privilegios del usuario y el contenido del menú."""
    
    user_data = {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }
    
    menu_data = get_privilege_content(user, privileges)
    privilege_list = list(privileges.keys())

    return jsonify({"usuario": user_data, "menu": menu_data, "privilegios": privilege_list}), 200
