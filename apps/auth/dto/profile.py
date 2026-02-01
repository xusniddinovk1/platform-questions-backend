from typing import TypedDict


class ProfileDTO(TypedDict):
    id: int
    email: str
    username: str
    first_name: str
    last_name: str


class ProfileRequestDTO(TypedDict):
    refresh_token: str | None
