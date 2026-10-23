from fastapi import FastAPI,Depends
from models import User
from routers.auth import router as auth_router
from dependencies import get_current_user,get_current_admin
from routers.products import router as products_router

app=FastAPI(title="Quickshop API")

app.include_router(auth_router)
app.include_router(products_router)

@app.get("/")
def home():
    return {"message":"Welcome to QuickShop API"}

@app.get("/auth/me")
def read_current_user(current_user:User=Depends(get_current_user)):
    return {
        "id":current_user.id,
        "email":current_user.email,
        "role":current_user.role.value
    }

@app.get("/admin/test")
def test_admin_access(current_admin:User=Depends(get_current_admin)):
    return {
        "message":"Admin access granted",
        "email":current_admin.email,
        "role":current_admin.role.value
    }