from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired

class RecuperarContrasenaForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])

class RestablecerContrasenaForm(FlaskForm):
    nueva_contrasena = PasswordField('Nueva contraseña', validators=[DataRequired()])
