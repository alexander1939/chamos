from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from app.features.contra.forms import RecuperarContrasenaForm, RestablecerContrasenaForm
from app.db.users_model import User
from app.db.db import db
from werkzeug.security import generate_password_hash


recovery_bp = Blueprint('recovery', __name__)

serializer = URLSafeTimedSerializer('UUr09BTA_9ZGHjl6Mz75FuUn-ftJli7yN2XMyt1myeA')

@recovery_bp.route('/recuperar-contrasena', methods=['GET', 'POST'])
def recuperar_contrasena():
    from app import mail  

    form = RecuperarContrasenaForm()
    if form.validate_on_submit():
        email = form.email.data
        usuario = User.query.filter_by(email=email).first()

        if usuario:
            token = serializer.dumps(email, salt='recover-password')
            recovery_link = url_for('recovery.restablecer_contrasena', token=token, _external=True)

            # Renderiza la plantilla del correo
            html_body = render_template('contra/recuperar_contra.jinja', recovery_link=recovery_link)

            msg = Message(
                'Recuperación de Contraseña',
                recipients=[email]
            )
            msg.html = html_body  # Usar HTML en lugar de texto plano

            try:
                mail.send(msg)
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
        email = serializer.loads(token, salt='recover-password', max_age=3600)
    except Exception:
        flash('El token ha expirado o es inválido.', 'danger')
        return redirect(url_for('recovery.recuperar_contrasena'))

    form = RestablecerContrasenaForm()
    if form.validate_on_submit():
        nueva_contrasena = form.nueva_contrasena.data
        usuario = User.query.filter_by(email=email).first()

        if usuario:
            hashed_password = generate_password_hash(nueva_contrasena, method='pbkdf2:sha256', salt_length=16)
            usuario.password = hashed_password
            db.session.commit()
            flash('Contraseña actualizada con éxito.', 'success')
            return redirect(url_for('auth.login'))  
        else:
            flash('No se ha encontrado un usuario con este correo.', 'danger')

    return render_template('contra/restablecer_contraseña.jinja', form=form)


@recovery_bp.route('/op_recuperacion')
def op_recuperacion():
    return render_template('contra/opcion_recuperacion.jinja')

@recovery_bp.route('/op_preguntas')
def op_preguntas():
    return render_template('contra/correo.jinja')

@recovery_bp.route('/recuperacion-preguntas', methods=['POST'])
def recuperacion_preguntas():
    email = request.form.get("email")

    if not email:
        flash("Correo electrónico requerido.", "danger")
        return redirect(url_for('recovery.op_preguntas'))  # Redirige a la vista del correo

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("El correo no está registrado.", "danger")
        return redirect(url_for('recovery.op_preguntas'))  # Redirige si no existe

    return redirect(url_for('recovery.preguntas_seguridad', email=email))


PREGUNTAS_SEGURIDAD = {
    "1": "¿Cuál es el nombre de tu primera mascota?",
    "2": "¿En qué ciudad naciste?",
    "3": "¿Cuál es tu comida favorita?",
    "4": "¿Cuál es el nombre de tu mejor amigo de la infancia?"
}

@recovery_bp.route('/preguntas-seguridad')
def preguntas_seguridad():
    email = request.args.get("email")

    if not email:
        flash("Correo electrónico no proporcionado.", "danger")
        return redirect(url_for('recovery.op_preguntas'))

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("El correo no está registrado.", "danger")
        return redirect(url_for('recovery.op_preguntas'))

    # Convertir el número en la pregunta correspondiente
    pregunta1_texto = PREGUNTAS_SEGURIDAD.get(str(user.pregunta1), "Pregunta desconocida")
    pregunta2_texto = PREGUNTAS_SEGURIDAD.get(str(user.pregunta2), "Pregunta desconocida")

    return render_template('contra/preguntas.jinja', email=email, pregunta1=pregunta1_texto, pregunta2=pregunta2_texto)



