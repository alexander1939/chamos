from app.features.auth.model import User
from app.db import db
from werkzeug.security import generate_password_hash

def create_admin_user():
    admin_email = "admin@admin.com"
    admin_password = "Admin123"
    admin_name = "Admin"
    admin_surnames = "Admin"
    admin_phone = "1234567890"  

    existing_admin = User.query.filter_by(email=admin_email).first()

    if not existing_admin:
        print("Creando el usuario administrador...")

        admin_user = User(
            email=admin_email,
            password=generate_password_hash(admin_password),
            name=admin_name,
            surnames=admin_surnames,
            phone=admin_phone,
            role="Admin"  
        )

        db.session.add(admin_user)
        db.session.commit()
        print(f"Usuario administrador {admin_name} creado con éxito.")
    else:
        print(f"El usuario administrador con el correo {admin_email} ya existe.")
