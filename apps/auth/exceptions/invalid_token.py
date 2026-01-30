class InvalidToken(Exception):
    def __init__(self, message: str = "Токен истёк или недействителен") -> None:
        super().__init__(message)
