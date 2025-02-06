from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from app.features.contra.forms import RecuperarContrasenaForm, RestablecerContrasenaForm
from app.db.users_model import User

recovery_bp = Blueprint('recovery', __name__)

serializer = URLSafeTimedSerializer('UUr09BTA_9ZGHjl6Mz75FuUn-ftJli7yN2XMyt1myeA')

@recovery_bp.route('/recuperar-contrasena', methods=['GET', 'POST'])
def recuperar_contrasena():
    from app import mail  # ✅ Importar dentro de la función

    form = RecuperarContrasenaForm()
    if form.validate_on_submit():
        email = form.email.data
        usuario = User.query.filter_by(email=email).first()

        if usuario:
            token = serializer.dumps(email, salt='recover-password')
            recovery_link = url_for('recovery.restablecer_contrasena', token=token, _external=True)

            msg = Message('Recuperación de Contraseña', recipients=[email])
            msg.body = f'Para restablecer tu contraseña, haz clic en el siguiente enlace: {recovery_link}'
            
            try:
                mail.send(msg)  # ✅ Asegurar que 'mail' está accesible aquí
                flash('Correo de recuperación enviado.', 'success')
            except Exception as e:
                flash(f'Error al enviar correo: {e}', 'danger')

            return redirect(url_for('recovery.recuperar_contrasena'))
        else:
            flash('El email no está registrado.', 'danger')

    return render_template('contra/recuperar_contraseña.jinja', form=form)

@recovery_bp.route('/restablecer/<token>', methods=['GET', 'POST'])
def restablecer_contrasena(token):
    try:
        # Verificar el token y obtener el email
        email = serializer.loads(token, salt='recover-password', max_age=3600)
    except Exception:
        flash('El token ha expirado o es inválido.', 'danger')
        return redirect(url_for('recovery.recuperar_contrasena'))

    form = RestablecerContrasenaForm()
    if form.validate_on_submit():
        nueva_contrasena = form.nueva_contrasena.data
        usuario = User.query.filter_by(email=email).first()  # <-- Aquí también usamos 'email'

        if usuario:
            usuario.password = nueva_contrasena  # Recuerda usar un hash para la contraseña
            db.session.commit()
            flash('Contraseña actualizada con éxito.', 'success')
            return redirect(url_for('auth.login'))  # Redirige a la página de inicio de sesión

    return render_template('contra/restablecer_contraseña.jinja', form=form)
