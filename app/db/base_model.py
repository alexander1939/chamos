from .db import db
from sqlalchemy import Column, Integer


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
