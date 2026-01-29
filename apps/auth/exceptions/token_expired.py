class TokenExpired(Exception):
    def __init__(self, message: str = "Token expired") -> None:
        super().__init__(message)
