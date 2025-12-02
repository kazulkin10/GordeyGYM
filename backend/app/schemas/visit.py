from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.models import VisitDirection


class VisitBase(BaseModel):
    client_id: int
    direction: VisitDirection
    admin_id: Optional[int] = None
    note: Optional[str] = None


class VisitCreate(VisitBase):
    pass


class Visit(VisitBase):
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True
