from typing import TypedDict


class RegisterEmailRequestDTO(TypedDict):
    username: str
    last_name: str
    first_name: str
    password: str
    email: str


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
