class InvalidCredentials(Exception):
    """Invalid credentials exception"""

    def __init__(self, message: str = "Неверный данные") -> None:
        super().__init__(message)
