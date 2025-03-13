from app.db import db
from app.db.users_model import User
from app.db.UserPrivilege_model import UserPrivilege
from app.db.Privilege_model import Privilege
from werkzeug.security import generate_password_hash

def create_admin_user():
    admin_email = "alexcifuentes72818@gmail.com"
    admin_password = "Admin123"
    admin_name = "Admin"
    admin_surnames = "User"
    admin_phone = "123456789"  

    existing_admin = User.query.filter_by(email=admin_email).first()

    if not existing_admin:
        print("Creando el usuario administrador...")

        admin_user = User(
            email=admin_email,
            password=generate_password_hash(admin_password),
            name=admin_name,
            surnames=admin_surnames,
            phone=admin_phone,
            role_id=1
        )

        db.session.add(admin_user)
        db.session.commit()
        db.session.refresh(admin_user)

        privileges = Privilege.query.filter(Privilege.id.in_([4])).all()
        for privilege in privileges:
            user_privilege = UserPrivilege(user_id=admin_user.id, privilege_id=privilege.id,can_create=0,can_edit=1,can_view=1,can_delete=0)
            db.session.add(user_privilege)

        db.session.commit()
        print(f"Usuario administrador {admin_name} creado con éxito con privilegios.")
