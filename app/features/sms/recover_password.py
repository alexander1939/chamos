from flask import Blueprint, flash, redirect, render_template, request, jsonify, url_for, current_app
from itsdangerous import URLSafeTimedSerializer
import requests
from app.db import db
from app.db.users_model import User
from app.db.pass_codes import PasswordResetCode
import random
import datetime
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from flask import session  

# RUTA PARA REDIRIGIR A FORMULARIO ENVIAR CODIGO
# href="{{ url_for('sms_recover.request_password_reset') }}">SMS Restablecimiento</a></p>

# Cargar variables de entorno
load_dotenv()

# Inicializa el Blueprint
sms_recover_bp = Blueprint('sms_recover', __name__)

# Función para generar un código aleatorio de 6 dígitos
def generar_codigo():
    return str(random.randint(100000, 999999))

@sms_recover_bp.route("/send-reset-code", methods=["POST"])
def send_reset_code():
    data = request.get_json()
    phone = data.get("phone")  # Recibe el número de teléfono

    user = User.query.filter_by(phone=phone).first()  # Busca por teléfono
    if not user:
        return jsonify({"error": "Número de teléfono no registrado"}), 400

    # Generar código
    codigo = generar_codigo()

    # Guardar el código en la base de datos
    reset_code = PasswordResetCode(user_id=user.id, code=codigo)
    db.session.add(reset_code)
    db.session.commit()

    # Enviar el SMS utilizando ClickSend
    try:
        url = "https://rest.clicksend.com/v3/sms/send"
        username = os.getenv("CLICKSEND_USERNAME")  # Tu usuario de ClickSend
        api_key = os.getenv("CLICKSEND_API_KEY")  # Tu API key de ClickSend
        
        payload = {
            "messages": [
                {
                    "source": "python",
                    "to": f"+52{phone}",  # Asegúrate de agregar el código de país
                    "body": f'Tu código de recuperación es {codigo}'
                }
            ]
        }

        response = requests.post(url, auth=(username, api_key), json=payload)

        if response.status_code != 200:
            return jsonify({"error": "Error al enviar el SMS", "details": response.json()}), 500
        
        print(f'Mensaje enviado a {phone}: {response.json()}')
    except Exception as e:
        return jsonify({"error": "Error al enviar el SMS", "details": str(e)}), 500

    return jsonify({"message": "Código enviado", "redirect_url": url_for('sms_recover.verify_code')}), 200




@sms_recover_bp.route("/verify-reset-code", methods=["POST"])
def verify_reset_code():
    data = request.get_json()
    phone = data.get("phone")  # Recibe el número de teléfono
    code = data.get("code")

    user = User.query.filter_by(phone=phone).first()  # Busca por teléfono
    if not user:
        return jsonify({"error": "Número de teléfono no registrado"}), 400

    reset_code = PasswordResetCode.query.filter_by(user_id=user.id, code=code).first()
    if not reset_code:
        return jsonify({"error": "Código incorrecto o expirado"}), 400

    # Verificar la validez del código según la fecha de creación
    if datetime.datetime.utcnow() - reset_code.created_at > datetime.timedelta(minutes=10):  # Cambia 2 a 10 (o el tiempo que desees)
        return jsonify({"error": "Código expirado"}), 400

    # Guardar el número de teléfono en la sesión
    session["reset_phone"] = phone

    # Redirigir a la página de restablecimiento de contraseña
    reset_url = url_for('sms_recover.reset_password', _external=True)
    
    print(f"Redirigiendo a: {reset_url}")  # Debugging

    return jsonify({"message": "Código válido, redirigiendo...", "reset_url": reset_url}), 200


@sms_recover_bp.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        # Obtener el número de teléfono desde la sesión
        phone = session.get("reset_phone")
        if not phone:
            flash("Sesión inválida o expirada", "danger")
            return redirect(url_for("sms_recover.request_password_reset"))

        user = User.query.filter_by(phone=phone).first()  # Buscar al usuario
        if not user:
            flash("Número de teléfono no registrado", "danger")
            return redirect(url_for("sms_recover.request_password_reset"))

        nueva_contrasena = request.form.get("password")
        confirmar_contrasena = request.form.get("confirm_password")

        if not nueva_contrasena or not confirmar_contrasena:
            flash("Debes completar ambos campos", "danger")
            return render_template("contra/reset_password.jinja")

        if nueva_contrasena != confirmar_contrasena:
            flash("Las contraseñas no coinciden", "danger")
            return render_template("contra/reset_password.jinja")

        # Actualizar la contraseña del usuario
        user.password = generate_password_hash(nueva_contrasena)
        db.session.commit()

        # Limpiar la sesión después de restablecer la contraseña
        session.pop("reset_phone", None)

        flash("Contraseña restablecida con éxito", "success")
        return redirect(url_for("auth.login"))  # Redirigir al login

    return render_template("contra/reset_password.jinja")


@sms_recover_bp.route('/request-password-reset', methods=['GET'])
def request_password_reset():
    return render_template("contra/send_reset_code.jinja")

@sms_recover_bp.route("/verify-code", methods=["GET"])
def verify_code():
    return render_template("contra/verify_reset_code.jinja")