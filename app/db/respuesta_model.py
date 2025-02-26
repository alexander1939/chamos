from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_model import BaseModel # Asegúrate de importar tu BaseModel

class Answer(BaseModel):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    response = Column(String(255), nullable=False)

    user = relationship('User')
    question = relationship('Question')

    def __repr__(self):
        return f'<Answer {self.response} (User {self.user_id}, Question {self.question_id})>'
