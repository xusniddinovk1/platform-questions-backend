from typing import TypedDict

from apps.user.dto import UserDTO


class LoginEmailRequestDTO(TypedDict):
    email: str
    password: str


class LoginResponseDTO(TypedDict):
    access_token: str
    refresh_token: str
    user: UserDTO
