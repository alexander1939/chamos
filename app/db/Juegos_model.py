from app.db.base_model import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin

class Juegos(BaseModel, UserMixin):
    __tablename__ = 'juegos'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True) 
    id_usuario = Column(Integer, ForeignKey('users.id'), nullable=False)

    usuario = relationship("User", backref="juegos")


    def __repr__(self):
        return f'<Juegos {self.nombre}  - Usuario ID: {self.id_usuario}>'   