from dataclasses import dataclass
from typing import TypedDict


class RefreshTokenRequestDTO(TypedDict):
    """
    Передавать токент только на mobile app в web(HTTP Only cookie)
    """

    refresh_token: str


class RefreshTokenResponseDTO(TypedDict):
    access_token: str
    refresh_token: str


@dataclass(frozen=True)
class JWTPayload:
    user_id: int
    exp: int
    iat: int
