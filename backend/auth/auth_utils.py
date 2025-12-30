from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

# =====================
# CONFIG
# =====================
SECRET_KEY = "CHANGE_THIS_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# =====================
# PASSWORD FUNCTIONS
# =====================
def hash_password(password: str):
    password_bytes = password.encode("utf-8")
    safe_bytes = password_bytes[:72]
    return pwd_context.hash(safe_bytes.decode("utf-8", errors="ignore"))



def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

# =====================
# TOKEN FUNCTIONS
# =====================
def create_token(email: str):
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
