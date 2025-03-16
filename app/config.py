# app/config.py
import os
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

class Config:
    # Configuración de Flask
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Configuración de la base de datos MySQL con pymysql
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_USER_PWD')}@"
        f"{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False