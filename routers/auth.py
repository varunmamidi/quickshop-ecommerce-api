from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import User, UserRole
from schemas import UserCreate, UserLogin, UserResponse, Token
from auth import hash_password, verify_password, create_access_token

router=APIRouter(prefix="/auth", tags=["Authentication"])

@router.post( "/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED,)
def register_user(user_data:UserCreate,db:Session=Depends(get_db)):
    #check whether email is already registered
    existing_user=(db.query(User)
                     . filter(User.email==user_data.email)
                     .first())
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        )
    #Hash the passsword before storing 
    new_user=User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role=UserRole.user,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", response_model=Token)
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    # Find the user by email
    user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    # Reject unknown emails and incorrect passwords
    if not user or not verify_password(
        user_data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create a token using the actual database user's ID and role
    access_token = create_access_token(
        user_id=user.id,
        role=user.role.value,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

