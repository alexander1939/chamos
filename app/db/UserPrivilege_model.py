from app.db.base_model import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

class UserPrivilege(BaseModel):
    __tablename__ = 'user_privileges'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    privilege_id = Column(Integer, ForeignKey('privileges.id'), nullable=False)
    assigned_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Nuevas columnas para permisos
    can_create = Column(Boolean, default=False, nullable=False)
    can_edit = Column(Boolean, default=False, nullable=False)
    can_view = Column(Boolean, default=False, nullable=False)
    can_delete = Column(Boolean, default=False, nullable=False)

    user = relationship('User', backref='user_privileges')
    privilege = relationship('Privilege', backref='user_privileges')

    # Evitar asignaciones duplicadas (usuario-privilegio)
    __table_args__ = (
        UniqueConstraint('user_id', 'privilege_id', name='_user_privilege_uc'),
    )

    def __repr__(self):
        return (
            f'<UserPrivilege user_id={self.user_id} privilege_id={self.privilege_id} '
            f'can_create={self.can_create} can_edit={self.can_edit} '
            f'can_view={self.can_view} can_delete={self.can_delete}>'
        )
