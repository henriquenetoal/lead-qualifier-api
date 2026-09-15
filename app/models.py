from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True)
    status = Column(String, default="novo")
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)     