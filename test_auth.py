
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)

password = "SecurePass123"

hashed = hash_password(password)

print("Original password:", password)
print("Stored hash:", hashed)
print("Correct password:", verify_password(password, hashed))
print("Wrong password:", verify_password("WrongPassword", hashed))

token = create_access_token(user_id=1, role="user")
print("JWT created:", bool(token))

decoded = decode_access_token(token)
print("User ID:", decoded["sub"])
print("Role:", decoded["role"])
