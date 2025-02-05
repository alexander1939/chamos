from app.db import db
from app.db.Privilege_model import Privilege  

def create_privileges():
    # Lista de privilegios que queremos verificar y crear
    privileges = [
        {"name": "Materias", "description": "Acceso a la gestión de materias"},
        {"name": "Juegos", "description": "Acceso a la gestión de juegos"},
        {"name": "Proyectos", "description": "Acceso a la gestión de proyectos"},
        {"name": "Gestionar Privilegios", "description": "Modificar y consultar los Privilegios de los usuarios"},
    ]

    for privilege_data in privileges:
        existing_privilege = Privilege.query.filter_by(name=privilege_data["name"]).first()
        
        if not existing_privilege:
            print(f"Creando el privilegio {privilege_data['name']}...")

            new_privilege = Privilege(
                name=privilege_data["name"],
                description=privilege_data["description"]
            )
            db.session.add(new_privilege)
            db.session.commit()
            print(f"Privilegio {privilege_data['name']} creado con éxito.")
        else:
            print(f"El privilegio {privilege_data['name']} ya existe.")
