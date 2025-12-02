import enum
from datetime import datetime, date
from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Boolean,
    Text,
)
from sqlalchemy.orm import relationship
from app.db.session import Base


class Role(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    operator = "operator"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(Enum(Role), default=Role.operator, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(255), nullable=False, index=True)
    gender = Column(String(20))
    date_of_birth = Column(Date)
    phone = Column(String(50), unique=True, index=True)
    email = Column(String(255))
    photo_path = Column(String(512))
    balance = Column(Numeric(12, 2), default=0)
    barcode = Column(String(128), unique=True, index=True)
    vip = Column(Boolean, default=False)
    notes = Column(Text)
    health_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    subscriptions = relationship("Subscription", back_populates="client")
    visits = relationship("Visit", back_populates="client")


class SubscriptionType(Base):
    __tablename__ = "subscription_types"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    price = Column(Numeric(12, 2), nullable=False)
    duration_days = Column(Integer)
    visit_count = Column(Integer)
    description = Column(Text)
    metadata_json = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    subscriptions = relationship("Subscription", back_populates="subscription_type")


class SubscriptionStatus(str, enum.Enum):
    active = "active"
    expired = "expired"
    canceled = "canceled"
    frozen = "frozen"


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    subscription_type_id = Column(Integer, ForeignKey("subscription_types.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    remaining_visits = Column(Integer)
    status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.active)
    payment_method = Column(String(50))
    amount_paid = Column(Numeric(12, 2))
    admin_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    client = relationship("Client", back_populates="subscriptions")
    subscription_type = relationship("SubscriptionType", back_populates="subscriptions")
    admin = relationship("User")


class VisitDirection(str, enum.Enum):
    in_ = "in"
    out = "out"


class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    admin_id = Column(Integer, ForeignKey("users.id"))
    direction = Column(Enum(VisitDirection), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    note = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="visits")
    admin = relationship("User")
