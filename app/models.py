# models.py
from sqlalchemy import Column, String, DateTime
from .database import Base
from datetime import datetime


class Campaign(Base):
    __tablename__ = "campaigns"

    code = Column(String, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
