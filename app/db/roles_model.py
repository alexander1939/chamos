from app.db.base_model import BaseModel
from sqlalchemy import Column, String, Integer

class Role(BaseModel):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<Role {self.name}>'
