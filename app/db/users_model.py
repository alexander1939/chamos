from app.db.base_model import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin

class User(BaseModel, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    reset_token = Column(String(256), nullable=True) # Nuevo campo
    name = Column(String(80), nullable=False)
    surnames = Column(String(255), nullable=False)
    phone = Column(String(15), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    role = relationship('Role')
    reset_codes = relationship('PasswordResetCode', back_populates='user')

    sessions = relationship('ActiveSession', back_populates='user', cascade='all, delete-orphan')
    session_settings = relationship("UserSessionSettings", uselist=False, back_populates="user")
    
    def __repr__(self):
        return f'<User {self.email} - Role: {self.role.name}>'
