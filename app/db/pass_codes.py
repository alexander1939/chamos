from app.db.base_model import BaseModel
from sqlalchemy import Boolean, Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime

class PasswordResetCode(BaseModel):
    __tablename__ = 'password_reset_codes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    code = Column(String(6), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    used = Column(Boolean, default=False)

    # Relación con el modelo User
    user = relationship('User', back_populates='reset_codes')

    def __repr__(self):
        return f'<PasswordResetCode {self.code} for User ID {self.user_id}>'
