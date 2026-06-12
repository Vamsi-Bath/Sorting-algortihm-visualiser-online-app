import base64
import hashlib
import hmac
import json
import os
import secrets
import time
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from .database import get_db
from .models import User

SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
TOKEN_TTL_SECONDS = 60 * 60 * 12
security = HTTPBearer()

def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 200_000)
    return f"pbkdf2_sha256${salt}${base64.b64encode(digest).decode()}"

def verify_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, salt, stored = stored_hash.split("$", 2)
        if algorithm != "pbkdf2_sha256":
            return False
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 200_000)
        calculated = base64.b64encode(digest).decode()
        return hmac.compare_digest(calculated, stored)
    except ValueError:
        return False

def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")

def _unb64(data: str) -> bytes:
    return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))

def create_token(user_id: int) -> str:
    payload = {"sub": user_id, "exp": int(time.time()) + TOKEN_TTL_SECONDS}
    payload_raw = _b64(json.dumps(payload, separators=(",", ":")).encode())
    sig = hmac.new(SECRET_KEY.encode(), payload_raw.encode(), hashlib.sha256).digest()
    return f"{payload_raw}.{_b64(sig)}"

def read_token(token: str) -> int:
    try:
        payload_raw, sig = token.split(".", 1)
        expected = _b64(hmac.new(SECRET_KEY.encode(), payload_raw.encode(), hashlib.sha256).digest())
        if not hmac.compare_digest(sig, expected):
            raise ValueError("bad signature")
        payload = json.loads(_unb64(payload_raw))
        if payload["exp"] < int(time.time()):
            raise ValueError("expired")
        return int(payload["sub"])
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token") from exc

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    user_id = read_token(credentials.credentials)
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
