from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint

from .database import Base


class RemoteQSO(Base):
    """QSO records that originate from remote services."""

    __tablename__ = "remote_qsos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    remote = Column(String, index=True)
    remote_id = Column(Integer, index=True)
    callsign = Column(String, index=True)
    frequency = Column(Float)
    mode = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint("remote", "remote_id"),)


class QSO(Base):
    __tablename__ = "qsos"

    id = Column(Integer, primary_key=True, index=True)
    callsign = Column(String, index=True)
    frequency = Column(Float)
    mode = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
