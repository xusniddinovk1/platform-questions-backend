from typing import TypedDict


class UserDTO(TypedDict):
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
