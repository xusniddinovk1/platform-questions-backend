from typing import NotRequired, TypedDict

from apps.user.models import User


class LoginInput(TypedDict):
    username: str
    password: str


class LoginOutput(TypedDict):
    user: NotRequired[User]


class RegisterDTO(TypedDict):
    username: str
    password: str
    email: str
    phone: str
