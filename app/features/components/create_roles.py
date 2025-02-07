from app.db import db
from app.db.roles_model import Role  

def create_roles():
    roles = ['Admin', 'Usuario']

    for role_name in roles:
        existing_role = Role.query.filter_by(name=role_name).first()
        
        if not existing_role:
            print(f"Creando el rol {role_name}...")

            new_role = Role(name=role_name)
            db.session.add(new_role)
            db.session.commit()
            print(f"Rol {role_name} creado con éxito.")


