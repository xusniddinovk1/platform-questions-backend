from apps.auth.dto.profile import ProfileDTO
from apps.auth.dto.token import JWTPayload
from apps.auth.services.jwt import JWTService
from apps.core.logger import LoggerType, get_logger_service
from apps.user.exceptions.user_not_found import UserNotFoundException
from apps.user.services.user import UserService


class ProfileService:
    user_service: UserService
    jwt_service: JWTService
    log: LoggerType

    def __init__(self, user_service: UserService, jwt_service: JWTService) -> None:
        self.user_service = user_service
        self.jwt_service = jwt_service
        self.log = get_logger_service(__name__)

    def get_user_profile(self, refresh_token: str) -> ProfileDTO:
        jwt_payload: JWTPayload = self.jwt_service.decode_token(refresh_token)
        user_id = jwt_payload.user_id

        user = self.user_service.get_user_by_id(user_id)

        if not user:
            self.log.error("User not found")
            raise UserNotFoundException(user_id)

        profile_dto: ProfileDTO = ProfileDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        return profile_dto
