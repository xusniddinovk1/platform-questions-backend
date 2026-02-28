class IsUserAlreadyExists(Exception):
    """
    Ошибка для обработки случая, когда пользователь c
    указанным идентификатором(email, phone) уже существует.
    """

    def __init__(self, identifier: str) -> None:
        super().__init__(
            f"Пользователь c таким идентификатором {identifier} уже существует"
        )
