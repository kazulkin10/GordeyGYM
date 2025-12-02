from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.subscription import (
    Subscription,
    SubscriptionCreate,
    SubscriptionUpdate,
    SubscriptionType,
    SubscriptionTypeCreate,
    SubscriptionTypeUpdate,
)
from app.core.security import get_current_user, get_db
from app.models.models import Subscription as SubscriptionModel, SubscriptionType as SubscriptionTypeModel, SubscriptionStatus, Client

router = APIRouter()


@router.post("/types", response_model=SubscriptionType)
def create_subscription_type(
    sub_type: SubscriptionTypeCreate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    exists = db.query(SubscriptionTypeModel).filter(SubscriptionTypeModel.name == sub_type.name).first()
    if exists:
        raise HTTPException(status_code=400, detail="Subscription type already exists")
    obj = SubscriptionTypeModel(**sub_type.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/types", response_model=List[SubscriptionType])
def list_subscription_types(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(SubscriptionTypeModel).order_by(SubscriptionTypeModel.name).all()


@router.put("/types/{type_id}", response_model=SubscriptionType)
def update_subscription_type(
    type_id: int, sub_type: SubscriptionTypeUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    obj = db.query(SubscriptionTypeModel).filter(SubscriptionTypeModel.id == type_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    for key, value in sub_type.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def _resolve_dates(sub_type: SubscriptionTypeModel, start: date) -> tuple[date, int | None]:
    end_date = None
    remaining_visits = None
    if sub_type.duration_days:
        end_date = start + timedelta(days=sub_type.duration_days)
    if sub_type.visit_count:
        remaining_visits = sub_type.visit_count
    return end_date, remaining_visits


@router.post("/", response_model=Subscription)
def add_subscription(
    sub: SubscriptionCreate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    client = db.query(Client).filter(Client.id == sub.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    sub_type = db.query(SubscriptionTypeModel).filter(SubscriptionTypeModel.id == sub.subscription_type_id).first()
    if not sub_type:
        raise HTTPException(status_code=404, detail="Subscription type not found")
    end_date, remaining_visits = _resolve_dates(sub_type, sub.start_date)
    obj = SubscriptionModel(
        client_id=sub.client_id,
        subscription_type_id=sub.subscription_type_id,
        start_date=sub.start_date,
        end_date=end_date,
        remaining_visits=remaining_visits,
        status=SubscriptionStatus.active,
        payment_method=sub.payment_method,
        amount_paid=sub.amount_paid,
        admin_id=user.id,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/client/{client_id}", response_model=List[Subscription])
def list_subscriptions(client_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return (
        db.query(SubscriptionModel)
        .filter(SubscriptionModel.client_id == client_id)
        .order_by(SubscriptionModel.start_date.desc())
        .all()
    )


@router.put("/{subscription_id}", response_model=Subscription)
def update_subscription(
    subscription_id: int, sub: SubscriptionUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    obj = db.query(SubscriptionModel).filter(SubscriptionModel.id == subscription_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Subscription not found")
    for key, value in sub.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj
