from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp

class RegisterForm(FlaskForm):
    # Validación para el nombre: solo letras (sin números ni caracteres especiales) y permite espacios
    name = StringField('Nombre', validators=[
        DataRequired(message="El nombre es obligatorio."),
        Length(min=2, max=50, message="El nombre debe tener entre 2 y 50 caracteres."),
        Regexp('^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$', message="El nombre solo puede contener letras y espacios.")
    ])

    # Validación para los apellidos: solo letras (sin números ni caracteres especiales) y permite espacios
    surnames = StringField('Apellidos', validators=[
        DataRequired(message="Los apellidos son obligatorios."),
        Length(min=2, max=50, message="Los apellidos deben tener entre 2 y 50 caracteres."),
        Regexp('^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$', message="Los apellidos solo pueden contener letras y espacios.")
    ])

    phone = StringField('Teléfono', validators=[
    DataRequired(),
    Length(min=10, max=10, message="Debe tener 10 caracteres"),
    Regexp(r'^\+?[0-9\s-]+$', message="El número de teléfono debe ser válido.")
])

    # Validación para el correo: debe ser un correo electrónico válido
    email = EmailField('Correo', validators=[
        DataRequired(message="El correo es obligatorio."),
        Email(message="Por favor, introduce un correo válido.")
    ])

    # Validación para la contraseña: debe tener al menos una minúscula, una mayúscula, un número y entre 8 y 50 caracteres
    password = PasswordField('Contraseña', validators=[
        DataRequired(message="La contraseña es obligatoria."),
        Length(min=8, max=50, message="La contraseña debe tener entre 8 y 50 caracteres."),
        Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', message="La contraseña debe tener al menos una letra mayúscula, una letra minúscula y un número.")
    ])

    submit = SubmitField('Crear cuenta')




class LoginForm(FlaskForm):
    email = EmailField('Correo', validators=[
        DataRequired(), 
        Email(message="Por favor, introduce un correo válido.")
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(), 
        Length(min=8, message="La contraseña debe tener al menos 8 caracteres.")
    ])
    submit = SubmitField('Iniciar sesión')
