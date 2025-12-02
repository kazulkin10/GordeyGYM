from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel
from app.models.models import SubscriptionStatus


class SubscriptionBase(BaseModel):
    client_id: int
    subscription_type_id: int
    start_date: date
    end_date: Optional[date] = None
    remaining_visits: Optional[int] = None
    status: SubscriptionStatus = SubscriptionStatus.active
    payment_method: Optional[str] = None
    amount_paid: Optional[float] = None
    admin_id: Optional[int] = None


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionUpdate(BaseModel):
    status: Optional[SubscriptionStatus] = None
    end_date: Optional[date] = None
    remaining_visits: Optional[int] = None


class SubscriptionTypeBase(BaseModel):
    name: str
    price: float
    duration_days: Optional[int] = None
    visit_count: Optional[int] = None
    description: Optional[str] = None
    metadata_json: Optional[str] = None


class SubscriptionTypeCreate(SubscriptionTypeBase):
    name: str


class SubscriptionTypeUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    duration_days: Optional[int] = None
    visit_count: Optional[int] = None
    description: Optional[str] = None
    metadata_json: Optional[str] = None


class Subscription(SubscriptionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class SubscriptionType(SubscriptionTypeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
