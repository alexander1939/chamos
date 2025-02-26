from app.db.base_model import BaseModel
from sqlalchemy import Column, Integer, String
from app.db.db import db

class Question(BaseModel):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    text = Column(String(255), nullable=False, unique=True)

    def __repr__(self):
        return f'<Question {self.text}>'

    @classmethod
    def insert_default_questions(cls):
        """ Inserta preguntas por defecto si no existen """
        default_questions = [
            "¿Cuál es el nombre de tu primera mascota?",
            "¿En qué ciudad naciste?",
            "¿Cuál es tu comida favorita?",
            "¿Cuál es el nombre de tu mejor amigo de la infancia?",
            "¿Cuál es tu película favorita?",
            "¿Cómo se llamaba tu primera escuela?"
        ]

        for text in default_questions:
            if not db.session.query(cls).filter_by(text=text).first():
                db.session.add(cls(text=text))
        
        db.session.commit()
