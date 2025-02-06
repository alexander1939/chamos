from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from app.features.contra.forms import RecuperarContrasenaForm, RestablecerContrasenaForm
from app.db.users_model import User

# Crear blueprint para la parte de recuperación
recovery_bp = Blueprint('recovery', __name__, template_folder='templates')

# Configuración del token
serializer = URLSafeTimedSerializer('mi_clave_secreta')

@recovery_bp.route('/recuperar-contrasena', methods=['GET', 'POST'])
def recuperar_contrasena():
    form = RecuperarContrasenaForm()
    if form.validate_on_submit():
        correo = form.email.data
        usuario = User.query.filter_by(email=email).first()

        if usuario:
            # Generar token para recuperación
            token = serializer.dumps(correo, salt='recover-password')
            recovery_link = url_for('recovery.restablecer_contrasena', token=token, _external=True)

            # Enviar correo con enlace para restablecer la contraseña
            msg = Message('Recuperación de Contraseña', recipients=[correo])
            msg.body = f'Para restablecer tu contraseña, haz clic en el siguiente enlace: {recovery_link}'
            mail.send(msg)
            flash('Correo de recuperación enviado.', 'success')
            return redirect(url_for('recovery.recuperar_contrasena'))
        else:
            flash('Correo no registrado.', 'danger')

    return render_template('contra/recuperar_contraseña.jinja', form=form)

@recovery_bp.route('/restablecer/<token>', methods=['GET', 'POST'])
def restablecer_contrasena(token):
    try:
        # Verificar el token y obtener el correo
        correo = serializer.loads(token, salt='recover-password', max_age=3600)
    except Exception:
        flash('El token ha expirado o es inválido.', 'danger')
        return redirect(url_for('recovery.recuperar_contrasena'))

    form = RestablecerContrasenaForm()
    if form.validate_on_submit():
        nueva_contrasena = form.nueva_contrasena.data
        usuario = User.query.filter_by(correo=correo).first()

        if usuario:
            usuario.contrasena = nueva_contrasena  # Recuerda usar un hash para la contraseña
            db.session.commit()
            flash('Contraseña actualizada con éxito.', 'success')
            return redirect(url_for('auth.login'))  # Redirige a la página de inicio de sesión

    return render_template('contra/restablecer_contraseña.jinja', form=form)
