from typing import TypedDict


class RegisterRequestDTO(TypedDict):
    username: str
    last_name: str
    first_name: str
    password: str
    email: str
    phone: str


class RegisterResponseDTO(TypedDict):
    access_token: str
    refresh_token: str
