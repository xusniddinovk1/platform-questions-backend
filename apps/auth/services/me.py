from apps.auth.dto.me import MeUpdateRequestDTO
from apps.auth.exceptions.invalid_token import InvalidToken
from apps.auth.services.email_confirmation import EmailConfirmationService
from apps.auth.services.jwt import JWTService
from apps.user.exceptions.user_not_found import UserNotFoundException
from apps.user.models import User
from apps.user.services.user import UserService


class MeService:
    def __init__(
        self,
        user_service: UserService,
        jwt_service: JWTService,
        email_confirmation_service: EmailConfirmationService,
    ) -> None:
        self.user_service = user_service
        self.jwt_service = jwt_service
        self.email_confirmation_service = email_confirmation_service

    def get_me(self, access_token: str) -> User | None:
        user_id = self.jwt_service.decode_token(access_token).user_id

        if not user_id:
            raise InvalidToken()

        user = self.user_service.get_user_by_id(user_id)

        if not user:
            return None

        return user

    def update_me(self, access_token: str, dto: MeUpdateRequestDTO) -> User:
        """
        Частичное обновление данных текущего пользователя.
        """
        user_id = self.jwt_service.decode_token(access_token).user_id

        if not user_id:
            raise InvalidToken()

        user = self.user_service.get_user_by_id(user_id)

        if not user:
            raise UserNotFoundException(user_id=user_id)

        if "username" in dto:
            user.username = dto["username"]

        if "email" in dto:
            user.email = dto["email"]
            user.is_active = False

        if "first_name" in dto:
            user.first_name = dto["first_name"]

        if "last_name" in dto:
            user.last_name = dto["last_name"]

        if "university" in dto:
            user.university = dto["university"]

        if "birthday" in dto:
            user.birthday = dto["birthday"]

        updated_user = self.user_service.update_user(user)

        if "email" in dto:
            self.email_confirmation_service.send_confirmation(updated_user)

        return updated_user
