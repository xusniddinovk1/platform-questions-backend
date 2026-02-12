from typing import cast

from apps.auth.dto import (
    LoginEmailRequestDTO,
    LoginResponseDTO,
    RegisterRequestDTO,
    RegisterResponseDTO,
)
from apps.auth.dto.register import RegisterEmailRequestDTO
from apps.auth.dto.token import RefreshTokenRequestDTO, RefreshTokenResponseDTO
from apps.auth.exceptions.invalid_credentials import InvalidCredentials
from apps.auth.exceptions.is_user_already_exists import IsUserAlreadyExists
from apps.auth.services.email_confirmation import EmailConfirmationService
from apps.auth.services.jwt import JWTService
from apps.user.dto import UserDTO
from apps.user.models import User
from apps.user.serializer import UserSerializer
from apps.user.services.user import UserService


class AuthService:
    def __init__(
        self,
        user_svc: UserService,
        jwt_svc: JWTService,
        email_confierm_svc: EmailConfirmationService,
    ) -> None:
        self.user_svc = user_svc
        self.jwt_svc = jwt_svc
        self.email_confierm_svc = email_confierm_svc

    def register_email(self, dto: RegisterEmailRequestDTO) -> RegisterResponseDTO:
        is_exists: bool = self.user_svc.is_user_exists(dto["email"])

        if is_exists:
            raise IsUserAlreadyExists()

        prepare_data: RegisterRequestDTO = RegisterRequestDTO(
            email=dto["email"],
            password=dto["password"],
            username=dto["username"],
            last_name=dto["last_name"],
            first_name=dto["first_name"],
            phone="",
        )

        new_user = self.user_svc.create_user(prepare_data)

        self.email_confierm_svc.send_confirmation(new_user)

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

    def refresh_token(self, dto: RefreshTokenRequestDTO) -> RefreshTokenResponseDTO:
        payload = self.jwt_svc.decode_token(dto["refresh_token"])

        user = self.user_svc.get_user_by_id(id=payload.user_id)
        if not user:
            raise InvalidCredentials()

        access_token = self.jwt_svc.create_access_token(user.id)
        refresh_token = self.jwt_svc.create_refresh_token(user.id)

        return RefreshTokenResponseDTO(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def authenticate_token(self, token: str) -> User | None:
        """Проверяем токен и возвращаем пользователя"""
        try:
            payload = self.jwt_svc.decode_token(token)
        except Exception as e:
            raise ValueError(str(e))

        user = self.user_svc.get_user_by_id(payload.user_id)
        if not user:
            raise ValueError("User not found")

        return user
