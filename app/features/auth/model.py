from app.db.base_model import BaseModel
from sqlalchemy import Column, String, Integer,INT
from flask_login import UserMixin

class User(BaseModel, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(80),  nullable=False)
    surnames = Column(String(255), nullable=False)
    phone = Column(String(15), nullable=False)  # Campo para teléfono
    role = Column(String(50), default='Usuario', nullable=False)  # Rol por defecto

    def __repr__(self):
        return f'<User {self.email} - Role: {self.role}>'