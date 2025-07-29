from datetime import datetime
from pydantic import BaseModel

class QSOBase(BaseModel):
    callsign: str
    frequency: float
    mode: str
    timestamp: datetime | None = None

class QSOCreate(QSOBase):
    pass

class QSOUpdate(QSOBase):
    pass

class QSO(QSOBase):
    id: int

    class Config:
        orm_mode = True
