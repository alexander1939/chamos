from app.features.auth.model import User
from app.db import db
from werkzeug.security import generate_password_hash

def create_small_user():
    small_email = "Rober@small.com"
    small_password = "Rober12345"
    small_name = "Rober"
    small_surnames = "Rober"
    small_phone = "1234567890"  

    existing_admin = User.query.filter_by(email=small_email).first()

    if not existing_admin:
        print("Creando el usuario Small...")

        admin_user = User(
            email=small_email,
            password=generate_password_hash(small_password),
            name=small_name,
            surnames=small_surnames,
            phone=small_phone,
            role="Small"  
        )

        db.session.add(admin_user)
        db.session.commit()
        print(f"Usuario administrador {small_name} creado con éxito.")
    else:
        print(f"El usuario administrador con el correo {small_email} ya existe.")
