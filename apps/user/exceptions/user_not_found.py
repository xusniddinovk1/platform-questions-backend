class UserNotFoundException(Exception):
    """Exception raised when a user is not found."""

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        self.message = f"User with ID {self.user_id} not found."
        super().__init__(self.message)
