class GoogleOAuthError(Exception):
    """Raised when the Google OAuth flow fails."""

    def __init__(self, message: str = "Google OAuth authentication failed") -> None:
        super().__init__(message)


class GoogleEmailNotVerified(Exception):
    """Raised when the Google account email is not verified."""

    def __init__(self, message: str = "Google account email is not verified") -> None:
        super().__init__(message)
