from apps.auth.exceptions.invalid_token import InvalidToken
from apps.auth.services.jwt import JWTService
from apps.user.models import User
from apps.user.services.user import UserService


class MeService:
    def __init__(self, user_service: UserService, jwt_service: JWTService) -> None:
        self.user_service = user_service
        self.jwt_service = jwt_service

    def get_me(self, access_token: str) -> User | None:
        user_id = self.jwt_service.decode_token(access_token).user_id

        if not user_id:
            raise InvalidToken()

        user = self.user_service.get_user_by_id(user_id)

        if not user:
            return None

        return user
