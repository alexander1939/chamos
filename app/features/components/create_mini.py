from app.features.auth.model import User
from app.db import db
from werkzeug.security import generate_password_hash

def create_mini_user():
    mini_email = "Jesus@mini.com"
    mini_password = "Jesus12345"
    mini_name = "Jesus"
    mini_surnames = "Jesus"
    mini_phone = "1234567890"  

    existing_admin = User.query.filter_by(email=mini_email).first()

    if not existing_admin:
        print("Creando el usuario mini...")

        admin_user = User(
            email=mini_email,
            password=generate_password_hash(mini_password),
            name=mini_name,
            surnames=mini_surnames,
            phone=mini_phone,
            role="Mini"  
        )

        db.session.add(admin_user)
        db.session.commit()
        print(f"Usuario administrador {mini_name} creado con éxito.")
    else:
        print(f"El usuario administrador con el correo {mini_email} ya existe.")
