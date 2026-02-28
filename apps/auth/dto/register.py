from typing import TypedDict

from apps.user.dto import UserDTO


class RegisterEmailRequestDTO(TypedDict):
    username: str
    last_name: str
    first_name: str
    password: str
    email: str
    birthday: str
    university: str


class RegisterRequestDTO(TypedDict):
    username: str
    last_name: str
    first_name: str
    password: str
    email: str
    phone: str
    birthday: str
    university: str


class RegisterResponseDTO(TypedDict):
    access_token: str
    refresh_token: str
    user: UserDTO
