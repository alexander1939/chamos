from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired, ValidationError
import re
from app.db.users_model import User  

def validar_contrasena(form, field):
    if not re.search(r'[A-Z]', field.data):  
        raise ValidationError('La contraseña debe contener al menos una letra mayúscula.')
    if not re.search(r'[a-z]', field.data): 
        raise ValidationError('La contraseña debe contener al menos una letra minúscula.')
    if not re.search(r'[0-9]', field.data): 
        raise ValidationError('La contraseña debe contener al menos un número.')
    if len(field.data) < 8: 
        raise ValidationError('La contraseña debe tener al menos 8 caracteres.')

class RecuperarContrasenaForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])

    def validate_email(form, field):
        email = field.data
        usuario = User.query.filter_by(email=email).first()
        if not usuario:
            raise ValidationError('El correo no está registrado.')

class RestablecerContrasenaForm(FlaskForm):
    nueva_contrasena = PasswordField('Nueva contraseña', validators=[DataRequired(), validar_contrasena])