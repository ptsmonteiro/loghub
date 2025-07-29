from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime

from .database import Base

class QSO(Base):
    __tablename__ = "qsos"

    id = Column(Integer, primary_key=True, index=True)
    callsign = Column(String, index=True)
    frequency = Column(Float)
    mode = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
