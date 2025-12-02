from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.visit import Visit
from app.schemas.visit import VisitCreate
from app.core.security import get_current_user, get_db
from app.models.models import Visit as VisitModel, Client, Subscription, SubscriptionStatus, VisitDirection
from app.core.config import get_settings

router = APIRouter()
settings = get_settings()


def _active_subscription(subscriptions):
    today = datetime.utcnow().date()
    for sub in subscriptions:
        if sub.status != SubscriptionStatus.active:
            continue
        if sub.end_date and sub.end_date < today:
            sub.status = SubscriptionStatus.expired
            continue
        if sub.remaining_visits is not None and sub.remaining_visits <= 0:
            continue
        if sub.end_date and sub.end_date >= today or sub.end_date is None:
            return sub
    return None


@router.post("/scan/{barcode}", response_model=Visit)
def scan_barcode(barcode: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    client = db.query(Client).filter(Client.barcode == barcode).first()
    if not client:
        raise HTTPException(status_code=404, detail="Card not registered")

    last_visit = (
        db.query(VisitModel)
        .filter(VisitModel.client_id == client.id)
        .order_by(VisitModel.timestamp.desc())
        .first()
    )
    now = datetime.utcnow()
    if last_visit and (now - last_visit.timestamp) < timedelta(seconds=settings.double_scan_seconds):
        raise HTTPException(status_code=400, detail="Duplicate scan ignored")

    active_sub = _active_subscription(client.subscriptions)
    if not active_sub and not settings.allow_entry_without_active_subscription:
        raise HTTPException(status_code=403, detail="No active subscription")

    direction = VisitDirection.in_
    if last_visit and last_visit.direction == VisitDirection.in_:
        direction = VisitDirection.out

    visit = VisitModel(client_id=client.id, admin_id=user.id, direction=direction)

    if active_sub and active_sub.remaining_visits is not None and direction == VisitDirection.in_:
        active_sub.remaining_visits -= 1

    db.add(visit)
    db.commit()
    db.refresh(visit)
    return visit


@router.get("/", response_model=List[Visit])
def list_visits(limit: int = 50, db: Session = Depends(get_db), user=Depends(get_current_user)):
    visits = db.query(VisitModel).order_by(VisitModel.timestamp.desc()).limit(limit).all()
    return visits


@router.post("/", response_model=Visit)
def create_visit(visit_in: VisitCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    visit = VisitModel(**visit_in.model_dump())
    db.add(visit)
    db.commit()
    db.refresh(visit)
    return visit
