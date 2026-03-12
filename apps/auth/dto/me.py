from typing import TypedDict


class MeResponseDTO(TypedDict):
    id: int
    username: str
    email: str
    last_name: str
    first_name: str
    is_active: bool
    role: str


class MeUpdateRequestDTO(TypedDict, total=False):
    """
    DTO для частичного обновления текущего пользователя.

    вce поля являются необязательными, т.к. используется PATCH.
    """

    username: str
    email: str
    first_name: str
    last_name: str
