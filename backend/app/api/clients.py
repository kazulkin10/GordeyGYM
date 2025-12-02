from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.client import Client, ClientCreate, ClientUpdate
from app.core.security import get_current_user, get_db
from app.models.models import Client as ClientModel

router = APIRouter()


def _get_client(db: Session, client_id: int) -> ClientModel:
    client = db.query(ClientModel).filter(ClientModel.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.post("/", response_model=Client)
def create_client(client_in: ClientCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if client_in.barcode:
        existing = db.query(ClientModel).filter(ClientModel.barcode == client_in.barcode).first()
        if existing:
            raise HTTPException(status_code=400, detail="Barcode already assigned")
    if client_in.phone:
        existing_phone = db.query(ClientModel).filter(ClientModel.phone == client_in.phone).first()
        if existing_phone:
            raise HTTPException(status_code=400, detail="Phone already registered")
    client = ClientModel(**client_in.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@router.get("/", response_model=List[Client])
def list_clients(query: str | None = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    q = db.query(ClientModel)
    if query:
        like = f"%{query}%"
        q = q.filter(
            (ClientModel.full_name.ilike(like))
            | (ClientModel.phone.ilike(like))
            | (ClientModel.barcode.ilike(like))
        )
    return q.order_by(ClientModel.full_name).all()


@router.get("/{client_id}", response_model=Client)
def get_client(client_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    client = _get_client(db, client_id)
    return client


@router.put("/{client_id}", response_model=Client)
def update_client(client_id: int, client_in: ClientUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    client = _get_client(db, client_id)
    if client_in.barcode and client_in.barcode != client.barcode:
        existing = db.query(ClientModel).filter(ClientModel.barcode == client_in.barcode).first()
        if existing:
            raise HTTPException(status_code=400, detail="Barcode already assigned")
    for key, value in client_in.model_dump(exclude_unset=True).items():
        setattr(client, key, value)
    db.commit()
    db.refresh(client)
    return client
