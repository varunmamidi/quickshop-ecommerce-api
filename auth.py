import os 
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import jwt
from pwdlib import PasswordHash

load_dotenv()

SECRET_KEY =os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

if not SECRET_KEY or len(SECRET_KEY) < 32:
    raise RuntimeError("JWT_SECRET_KEY must be set and at least 32 characters long.")

password_hash=PasswordHash.recommended()

#Hash password before storing it in the database
def hash_password(password: str) -> str:
    return password_hash.hash(password)

#Verify password against the hashed password stored in the database
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return password_hash.verify(plain_password, hashed_password)
    except Exception:
        return False

#Generate JWT token for user authentication
def create_access_token(user_id:int, role: str)->str:
    expire_at=datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload={
        "sub":str(user_id),
        "role":role,
        "exp":expire_at
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

#Decode and verify JWT token
def decode_access_token(token:str)->dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])