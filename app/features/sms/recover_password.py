import sqlite3
from twilio.rest import Client
import random

# Configuración de Twilio
account_sid = 'your_account_sid'  # Reemplaza con tu Account SID de Twilio
auth_token = 'your_auth_token'    # Reemplaza con tu Auth Token de Twilio
twilio_phone_number = '+1234567890'  # Reemplaza con tu número de Twilio

# Inicializar el cliente de Twilio
client = Client(account_sid, auth_token)

# Función para generar un código aleatorio
def generate_verification_code():
    return random.randint(1000, 9999)  # Código de 4 dígitos

# Función para enviar el código por SMS
def send_verification_code(phone_number, code):
    message = client.messages.create(
        body=f"Tu código de verificación es: {code}",
        from_=twilio_phone_number,
        to=phone_number
    )
    return message.sid

# Función para recuperar contraseña
def recover_password(email):
    # Conectar a la base de datos
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    # Buscar el usuario por email
    cursor.execute("SELECT id, phone FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    if user:
        user_id, phone_number = user
        verification_code = generate_verification_code()

        # Guardar el código en la base de datos (en una tabla de códigos de verificación)
        cursor.execute("INSERT INTO verification_codes (user_id, code) VALUES (?, ?)", (user_id, verification_code))
        conn.commit()

        # Enviar el código por SMS
        message_sid = send_verification_code(phone_number, verification_code)
        print(f"Código de verificación enviado a {phone_number}. Message SID: {message_sid}")
    else:
        print("No se encontró un usuario con ese email.")

    # Cerrar la conexión a la base de datos
    conn.close()

# Función para validar el código y restablecer la contraseña
def reset_password(email, code, new_password):
    # Conectar a la base de datos
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    # Buscar el usuario por email
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    if user:
        user_id = user[0]

        # Buscar el código de verificación en la base de datos
        cursor.execute("SELECT code FROM verification_codes WHERE user_id = ? AND code = ?", (user_id, code))
        saved_code = cursor.fetchone()

        if saved_code:
            # Actualizar la contraseña del usuario
            cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, user_id))
            conn.commit()

            # Eliminar el código de verificación (ya no es necesario)
            cursor.execute("DELETE FROM verification_codes WHERE user_id = ?", (user_id,))
            conn.commit()

            print("Contraseña restablecida exitosamente.")
        else:
            print("Código de verificación incorrecto.")
    else:
        print("No se encontró un usuario con ese email.")

    # Cerrar la conexión a la base de datos
    conn.close()

# Ejemplo de uso
email = "usuario@example.com"  # Esto podría venir de un formulario o solicitud API
recover_password(email)  # Envía el código de verificación

# Supongamos que el usuario ingresa el código y una nueva contraseña
user_code = int(input("Ingresa el código de verificación: "))  # Código que el usuario recibe
new_password = input("Ingresa tu nueva contraseña: ")  # Nueva contraseña
reset_password(email, user_code, new_password)  # Valida el código y restablece la contraseña