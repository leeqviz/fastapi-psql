from datetime import timedelta

import bcrypt
import jwt

from src.configs import settings
from src.utils import timestamp_with_tz


def encode_jwt(
    payload: dict,
    private_key: str = settings.jwt.private_key_path.read_text(),
    algorithm: str = settings.jwt.algorithm,
):
    encoded = jwt.encode(payload, private_key, algorithm=algorithm)
    return encoded


def create_access_token(
    payload: dict,
    expires_in: int = settings.jwt.access_token_expire_minutes,
    expires_delta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = timestamp_with_tz
    expire = now + (expires_delta or timedelta(minutes=expires_in))

    to_encode.update(
        {
            # "sub": payload["name"],
            "exp": expire,
            "iat": now,
        }
    )
    return encode_jwt(to_encode)


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.jwt.public_key_path.read_text(),
    algorithm: str = settings.jwt.algorithm,
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)
