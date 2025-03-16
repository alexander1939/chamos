from app.db import db
from app.db.users_model import User
from app.db.UserPrivilege_model import UserPrivilege
from app.db.Privilege_model import Privilege
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

def create_admin_user():
    # Obtener las variables de entorno
    admin_email = os.getenv('ADMIN_EMAIL')
    admin_password = os.getenv('ADMIN_PASSWORD')
    admin_name = os.getenv('ADMIN_NAME')
    admin_surnames = os.getenv('ADMIN_SURNAMES')
    admin_phone = os.getenv('ADMIN_PHONE')
    admin_role_id = int(os.getenv('ADMIN_ROLE_ID'))
    admin_privilege_ids = list(map(int, os.getenv('ADMIN_PRIVILEGE_IDS').split(',')))

    # Verificar si el administrador ya existe
    existing_admin = User.query.filter_by(email=admin_email).first()

    if not existing_admin:
        print("Creando el usuario administrador...")

        # Crear el usuario administrador
        admin_user = User(
            email=admin_email,
            password=generate_password_hash(admin_password),
            name=admin_name,
            surnames=admin_surnames,
            phone=admin_phone,
            role_id=admin_role_id
        )

        db.session.add(admin_user)
        db.session.commit()
        db.session.refresh(admin_user)

        # Asignar privilegios al administrador
        privileges = Privilege.query.filter(Privilege.id.in_(admin_privilege_ids)).all()
        for privilege in privileges:
            user_privilege = UserPrivilege(
                user_id=admin_user.id,
                privilege_id=privilege.id,
                can_create=0,
                can_edit=1,
                can_view=1,
                can_delete=0
            )
            db.session.add(user_privilege)

        db.session.commit()
        print(f"Usuario administrador {admin_name} creado con éxito con privilegios.")
    else:
        print("El usuario administrador ya existe.")