from app.db.base_model import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class ActiveSession(BaseModel):
    __tablename__ = 'active_sessions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='sessions')

    def __repr__(self):
        return f'<ActiveSession {self.id} - User ID: {self.user_id} - IP: {self.ip_address} - Agent: {self.user_agent}>'
