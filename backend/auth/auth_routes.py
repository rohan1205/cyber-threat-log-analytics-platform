from fastapi import APIRouter, HTTPException
from auth.models import UserRegister, UserLogin
from auth.auth_utils import hash_password, verify_password, create_token

router = APIRouter(prefix="/auth", tags=["Auth"])

# TEMP in-memory storage (OK for now)
users_db = {}

@router.post("/register")
def register(user: UserRegister):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    users_db[user.email] = {
        "email": user.email,
        "password": hash_password(user.password)
    }

    return {"message": "User registered successfully"}

@router.post("/login")
def login(user: UserLogin):
    saved_user = users_db.get(user.email)

    if not saved_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, saved_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(user.email)
    return {
        "access_token": token,
        "token_type": "bearer"
    }
