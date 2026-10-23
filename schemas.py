from pydantic import BaseModel, Field, EmailStr, ConfigDict
from models import ProductCategory


# USER SCHEMAS
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

#PRODUCT SCHEMAS
class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    category: ProductCategory

class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str | None
    price: float
    stock: int
    category: ProductCategory