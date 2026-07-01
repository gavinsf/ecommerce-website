from sqlalchemy import Column, String, Float, Integer, ForeignKey, Enum, DateTime
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
import datetime


class OrderStatus(enum.Enum):
    pending   = "pending"
    paid      = "paid"
    shipped   = "shipped"
    cancelled = "cancelled"

class User(Base):
    __tablename__ = "users"
    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email         = Column(String, unique=True, nullable=False)
    hash          = Column(String, nullable=False)
    created_at    = Column(DateTime, default=datetime.datetime.now)
    is_admin      = Column(Integer, default=0, nullable=False)

class Product(Base):
    __tablename__ = "products"
    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name          = Column(String, nullable=False)
    cost_price    = Column(Float, nullable=False)
    sell_price    = Column(Float, nullable=False)
    created_at    = Column(DateTime, default=datetime.datetime.now)
    is_deleted    = Column(Integer, default=0)
    stock         = Column(Integer, default=0)

class Order(Base):
    __tablename__ = "orders"
    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id       = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    status        = Column(Enum(OrderStatus), default=OrderStatus.pending)
    total         = Column(Float)
    created_at    = Column(DateTime, default=datetime.datetime.now)

class OrderItem(Base):
    __tablename__ = "order_items"
    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id      = Column(UUID(as_uuid=True), ForeignKey("orders.id"))
    product_id    = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    quantity      = Column(Integer)
    unit_price    = Column(Float)

class CartItem(Base):
    __tablename__ = "cart_items"
    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id       = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    product_id    = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    quantity      = Column(Integer, nullable=False, default=1)
    created_at    = Column(DateTime, default=datetime.datetime.now)
    