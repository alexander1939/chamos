from datetime import datetime, timedelta
from flask import flash

MAX_FAILED_ATTEMPTS = 3  # Límite de intentos fallidos
TIME_LIMIT = timedelta(minutes=1)  # Tiempo de espera de 1 minuto

# Diccionario para almacenar los intentos fallidos y la última vez que intentó el usuario
failed_attempts_cache = {}

def validar_intentos_preguntas(email):
    """
    Valida si un usuario puede realizar intentos de preguntas
    teniendo en cuenta el número de intentos fallidos y el tiempo de espera.
    """
    bloqueo_hasta = None

    if email in failed_attempts_cache:
        user_data = failed_attempts_cache[email]

        if user_data['failed_attempts'] >= MAX_FAILED_ATTEMPTS:
            tiempo_restante = TIME_LIMIT - (datetime.now() - user_data['last_failed_attempt'])

            if tiempo_restante.total_seconds() > 0:
                bloqueo_hasta = (datetime.now() + tiempo_restante).timestamp()  # Enviar timestamp UNIX
                flash("Demasiados intentos fallidos. Intenta de nuevo en 1 minuto.", "warning")
                return False, bloqueo_hasta
            else:
                failed_attempts_cache[email] = {'failed_attempts': 0, 'last_failed_attempt': None}

    return True, bloqueo_hasta


def registrar_intento_fallido(email):
    """
    Registra un intento fallido de un usuario.
    Si no tiene intentos registrados, lo crea.
    """
    if email in failed_attempts_cache:
        user_data = failed_attempts_cache[email]
        user_data['failed_attempts'] += 1
        user_data['last_failed_attempt'] = datetime.now()
    else:
        # Si el usuario no tiene intentos registrados, crear un nuevo registro
        failed_attempts_cache[email] = {'failed_attempts': 1, 'last_failed_attempt': datetime.now()}
