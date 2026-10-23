from sqlalchemy import Column, Integer, String, Float, Enum
from database import Base
import enum


class UserRole(str, enum.Enum):
    admin="admin"
    user="user"


class ProductCategory(str, enum.Enum):
    electronics="electronics"
    fashion="fashion"
    grocery="grocery"
    books="books"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    stock=Column(Integer, nullable=False)
    category=Column(Enum(ProductCategory), nullable=False)