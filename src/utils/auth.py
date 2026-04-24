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


def issue_token(
    subject: str,
    token_type: str,
    expires_in: int,
    extra_claims: dict | None = None,
):

    payload = {
        "sub": subject,
        "iss": settings.app.name,
        "exp": int((timestamp_with_tz + timedelta(minutes=expires_in)).timestamp()),
        "iat": int(timestamp_with_tz.timestamp()),
        "nbf": int(timestamp_with_tz.timestamp()),
        "type": token_type,
    }

    if extra_claims:
        payload.update(extra_claims)

    return encode_jwt(payload)


def issue_access_token(
    subject: str,
    extra_claims: dict | None = None,
    expires_in: int = settings.jwt.access_token_expire_minutes,
):
    return issue_token(subject, "access", expires_in, extra_claims)


def issue_refresh_token(
    subject: str,
    extra_claims: dict | None = None,
    expires_in: int = settings.jwt.refresh_token_expire_minutes,
):
    return issue_token(subject, "refresh", expires_in, extra_claims)


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
