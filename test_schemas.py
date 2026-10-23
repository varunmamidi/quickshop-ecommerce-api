
from schemas import UserCreate, ProductCreate

user = UserCreate(
    email="user@example.com",
    password="SecurePass123"
)
print("User validation:", user.email)

product = ProductCreate(
    name="Laptop",
    description="A test laptop",
    price=50000,
    stock=10,
    category="electronics"
)
print("Product validation:", product.model_dump())
