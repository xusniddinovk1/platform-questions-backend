from typing import cast

from apps.auth.dto import (
    LoginEmailRequestDTO,
    LoginResponseDTO,
    RegisterRequestDTO,
    RegisterResponseDTO,
)
from apps.auth.exceptions.invalid_credentials import InvalidCredentials
from apps.auth.exceptions.is_user_already_exists import IsUserAlreadyExists
from apps.auth.services.cookie import CookieService
from apps.auth.services.jwt import JWTService
from apps.user.dto import UserDTO
from apps.user.serializer import UserSerializer
from apps.user.services.user import UserService


class AuthService:
    def __init__(
        self, user_svc: UserService, cookie_svc: CookieService, jwt_svc: JWTService
    ) -> None:
        self.user_svc = user_svc
        self.cookie_svc = cookie_svc
        self.jwt_svc = jwt_svc

    def register_email(self, dto: RegisterRequestDTO) -> RegisterResponseDTO:
        is_exists: bool = self.user_svc.is_user_exists(dto["email"])

        if is_exists:
            raise IsUserAlreadyExists()

        new_user = self.user_svc.create_user(dto)
        access_token = self.jwt_svc.create_access_token(new_user.id)
        refresh_token = self.jwt_svc.create_refresh_token(new_user.id)

        return RegisterResponseDTO(access_token=access_token, refresh_token=refresh_token)

    def login_email(self, dto: LoginEmailRequestDTO) -> LoginResponseDTO:
        user = self.user_svc.get_user_by_email(dto["email"])
        if not user or not user.check_password(dto["password"]):
            raise InvalidCredentials()

        access_token = self.jwt_svc.create_access_token(user.id)
        refresh_token = self.jwt_svc.create_refresh_token(user.id)

        user_data: UserDTO = cast(UserDTO, UserSerializer(user).data)

        return LoginResponseDTO(
            access_token=access_token, refresh_token=refresh_token, user=user_data
        )
