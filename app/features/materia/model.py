from app.db.base_model import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class Materia(BaseModel, UserMixin):
    __tablename__ = 'materias'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True) 
    docente = Column(String(120), nullable=False)  
    creditos = Column(Integer, nullable=False)  
    semestre = Column(String(20), nullable=False)  
    id_usuario = Column(Integer, ForeignKey('users.id'), nullable=False)


    def __repr__(self):
        return f'<Materia {self.nombre} - Docente: {self.docente} - Usuario ID: {self.id_usuario}>'
