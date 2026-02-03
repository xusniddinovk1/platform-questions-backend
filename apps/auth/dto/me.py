from typing import TypedDict


class MeResponseDTO(TypedDict):
    id: int
    username: str
    email: str
    last_name: str
    first_name: str
    is_active: bool
    role: str
