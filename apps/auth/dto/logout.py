from typing import TypedDict


class LogoutRequestDto(TypedDict):
    refresh_token: str
