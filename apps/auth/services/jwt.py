from datetime import datetime, timedelta

import jwt

from apps.auth.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_ALGORITHM,
    JWT_SECRET,
    REFRESH_TOKEN_EXPIRE_DAYS,
)
from apps.auth.dto.token import JWTPayload
from apps.auth.exceptions.invalid_token import InvalidToken
from apps.auth.exceptions.token_expired import TokenExpired


class JWTService:
    def __init__(self) -> None:
        self.access_token_expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES
        self.jwt_algorithm = JWT_ALGORITHM
        self.jwt_secret = JWT_SECRET
        self.refresh_token_expire_days = REFRESH_TOKEN_EXPIRE_DAYS

    def create_access_token(self, user_id: int) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            "iat": datetime.utcnow(),
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    def create_refresh_token(self, user_id: int) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
            "iat": datetime.utcnow(),
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    def decode_token(self, token: str) -> JWTPayload:
        try:
            payload = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=[self.jwt_algorithm],
            )
            return JWTPayload(
                user_id=payload["user_id"],
                exp=payload["exp"],
                iat=payload["iat"],
            )
        except jwt.ExpiredSignatureError:
            raise TokenExpired()
        except jwt.DecodeError:
            raise InvalidToken()
