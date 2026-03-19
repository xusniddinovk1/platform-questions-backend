from typing import TypedDict

from apps.user.dto import UserDTO


class GoogleAuthURLResponseDTO(TypedDict):
    authorization_url: str


class GoogleCallbackRequestDTO(TypedDict):
    code: str
    state: str


class GoogleUserInfoDTO(TypedDict):
    sub: str
    email: str
    email_verified: bool
    given_name: str
    family_name: str
    picture: str


class GoogleCallbackResponseDTO(TypedDict):
    access_token: str
    refresh_token: str
    user: UserDTO
    is_new_user: bool
