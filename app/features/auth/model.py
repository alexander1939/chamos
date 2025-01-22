from app.db.base_model import BaseModel
from sqlalchemy import Column, String, Integer
from flask_login import UserMixin
from sqlalchemy.orm import relationship

class User(BaseModel, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    role = Column(String(1000), nullable=False)


    def __repr__(self):
        return f'<User {self.username}>'