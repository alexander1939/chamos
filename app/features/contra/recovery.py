from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from app.features.contra.forms import RecuperarContrasenaForm, RestablecerContrasenaForm
from app.db.db import db
from werkzeug.security import generate_password_hash
import secrets
from app.db.users_model import User
from app.db.respuesta_model import Answer
from app.db.preguntas_model import Question
from app.middleware.contra_middleware import validar_intentos_preguntas, registrar_intento_fallido


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
        return redirect(url_for('recovery.op_preguntas'))

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("El correo no está registrado.", "danger")
        return redirect(url_for('recovery.op_preguntas'))

    # Generar un token seguro y almacenarlo en la base de datos
    token = secrets.token_urlsafe(32)  # Genera un token seguro
    user.reset_token = token
    db.session.commit()  # Guarda el token en la base de datos

    # Traer respuestas de seguridad
    answers = Answer.query.filter_by(user_id=user.id).join(Question, Answer.question_id == Question.id).all()

    if len(answers) < 2:
        flash("El usuario no tiene suficientes preguntas de seguridad registradas.", "danger")
        return redirect(url_for('recovery.op_preguntas'))

    preguntas = [(answer.question.id, answer.question.text) for answer in answers]

    return render_template('contra/preguntas.jinja', token=token, preguntas=preguntas)


    


@recovery_bp.route('/verificar-respuestas', methods=['POST'])
def verificar_respuestas():
    token = request.form.get("token")

    if not token:
        flash("Token inválido.", "danger")
        return redirect(url_for('recovery.op_preguntas'))

    user = User.query.filter_by(reset_token=token).first()

    if not user:
        flash("El token ha expirado o es inválido.", "danger")
        return redirect(url_for('recovery.op_preguntas'))

    puede_intentar, bloqueo_hasta = validar_intentos_preguntas(user.email)
    
    if not puede_intentar:
        return render_template(
            'contra/preguntas.jinja', 
            token=token, 
            preguntas=[(answer.question.id, answer.question.text) for answer in Answer.query.filter_by(user_id=user.id).all()], 
            bloqueo_hasta=bloqueo_hasta
        )

    answers = Answer.query.filter_by(user_id=user.id).all()

    if not answers:
        flash("No hay respuestas registradas para este usuario.", "danger")
        return redirect(url_for('recovery.op_preguntas'))

    correctas = 0
    for answer in answers:
        user_input = request.form.get(str(answer.question_id), "").strip().lower()
        correct_answer = answer.response.strip().lower()

        if user_input == correct_answer:
            correctas += 1

    if correctas >= 2:
        flash("Respuestas correctas. Puede restablecer su contraseña.", "success")
        return redirect(url_for('recovery.restablecer_contra', token=token))
    else:
        registrar_intento_fallido(user.email)
        flash("Las respuestas no son correctas. Intente de nuevo.", "danger")
        return render_template(
            'contra/preguntas.jinja', 
            token=token, 
            preguntas=[(answer.question.id, answer.question.text) for answer in answers],
            bloqueo_hasta=bloqueo_hasta
        )


@recovery_bp.route('/restablecer-contra', methods=['GET', 'POST'])
def restablecer_contra():
    token = request.args.get("token")

    if not token:
        flash("Token inválido o ausente.", "danger")
        return redirect(url_for('recovery.op_preguntas'))

    user = User.query.filter_by(reset_token=token).first()

    if not user:
        flash("El token ha expirado o es inválido.", "danger")
        return redirect(url_for('recovery.op_preguntas'))

    if request.method == 'POST':
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not new_password or not confirm_password:
            flash("Todos los campos son obligatorios.", "danger")
            return redirect(url_for('recovery.restablecer_contra', token=token))

        if new_password != confirm_password:
            flash("Las contraseñas no coinciden.", "danger")
            return redirect(url_for('recovery.restablecer_contra', token=token))

        # Generar el hash de la nueva contraseña
        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=16)

        # Asignar la nueva contraseña e invalidar el token
        user.password = hashed_password
        user.reset_token = None  # Invalidar token

        try:
            db.session.commit()
            flash("Contraseña restablecida con éxito.", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar la contraseña: {e}", "danger")
            return redirect(url_for('recovery.restablecer_contra', token=token))

    return render_template('contra/res_contraseña.jinja', token=token)
