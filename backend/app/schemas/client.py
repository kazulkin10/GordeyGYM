from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from app.schemas.subscription import Subscription
from app.schemas.visit import Visit


class ClientBase(BaseModel):
    full_name: str
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    photo_path: Optional[str] = None
    balance: Optional[float] = 0
    barcode: Optional[str] = None
    vip: bool = False
    notes: Optional[str] = None
    health_notes: Optional[str] = None


class ClientCreate(ClientBase):
    full_name: str


class ClientUpdate(ClientBase):
    pass


class Client(ClientBase):
    id: int
    created_at: datetime
    subscriptions: List[Subscription] = []
    visits: List[Visit] = []

    class Config:
        from_attributes = True
