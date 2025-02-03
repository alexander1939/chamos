from app.db.base_model import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, UniqueConstraint  # Añadir UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

class UserPrivilege(BaseModel):
    __tablename__ = 'user_privileges'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    privilege_id = Column(Integer, ForeignKey('privileges.id'), nullable=False)
    assigned_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship('User', backref='user_privileges')
    privilege = relationship('Privilege', backref='user_privileges')

    # Evitar asignaciones duplicadas (usuario-privilegio)
    __table_args__ = (
        UniqueConstraint('user_id', 'privilege_id', name='_user_privilege_uc'),
    )

    def __repr__(self):
        return f'<UserPrivilege user_id={self.user_id} privilege_id={self.privilege_id}>'