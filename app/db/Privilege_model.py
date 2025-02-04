from app.db.base_model import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

class Privilege(BaseModel):
    __tablename__ = 'privileges'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    def __repr__(self):
        return f'<Privilege {self.name}>'