class IsUserAlreadyExists(Exception):
    """
    Ошибка для обработки случая, когда пользователь c
    указанным идентификатором(email, phone) уже существует.
    """

    def __init__(self) -> None:
        super().__init__("Пользователь c таким идентификатором уже существует")
