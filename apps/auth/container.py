from apps.auth.services.auth import AuthService
from apps.auth.services.confirmation_link import ConfirmationLinkService
from apps.auth.services.cookie import CookieService
from apps.auth.services.email_confirmation import (
    EmailConfirmationActivationService,
    EmailConfirmationService,
)
from apps.auth.services.jwt import JWTService
from apps.auth.services.me import MeService
from apps.auth.services.profile import ProfileService
from apps.auth.tokens.django import DjangoTokenGenerator
from apps.core.container import get_config_service
from apps.core.logger import get_logger_service
from apps.notifications.services.email import EmailSenderService
from apps.user.container import get_user_service


def get_jwt_service() -> JWTService:
    return JWTService()


def get_cookie_service() -> CookieService:
    return CookieService()


def get_auth_service() -> AuthService:
    jwt_svc = get_jwt_service()
    user_svc = get_user_service()
    confeirm_svc = get_confirmation_service()
    svc = AuthService(user_svc, jwt_svc, confeirm_svc)
    return svc


def get_profile_service() -> ProfileService:
    user_svc = get_user_service()
    jwt_svc = get_jwt_service()
    svc = ProfileService(user_svc, jwt_svc)

    return svc


def get_confirmation_service() -> EmailConfirmationService:
    cfg = get_config_service()
    sender = EmailSenderService(cfg)
    token_generator = DjangoTokenGenerator()
    link_service = ConfirmationLinkService(token_generator, cfg)

    log = get_logger_service("email_confirmation_service")

    service = EmailConfirmationService(sender, link_service, log)

    return service


def get_confirmation_activation_service() -> EmailConfirmationActivationService:
    token_generator = DjangoTokenGenerator()
    service = EmailConfirmationActivationService(token_generator=token_generator)
    return service


def get_me_service() -> MeService:
    user_svc = get_user_service()
    jwt_svc = get_jwt_service()
    svc = MeService(user_svc, jwt_svc)
    return svc
