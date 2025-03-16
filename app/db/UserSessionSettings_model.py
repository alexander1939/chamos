from app.db.base_model import BaseModel
from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class UserSessionSettings(BaseModel):
    __tablename__ = 'user_session_settings'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    allow_multiple_sessions = Column(Boolean, default=True, nullable=False)
    enable_2fa = Column(Boolean, default=True, nullable=False)  # 🔹 Nuevo campo para activar/desactivar 2FA

    user = relationship("User", back_populates="session_settings")

    def __repr__(self):
        return (f"<UserSessionSettings user_id={self.user_id} "
                f"allow_multiple_sessions={self.allow_multiple_sessions} "
                f"enable_2fa={self.enable_2fa}>")
