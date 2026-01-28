from apps.auth.services.auth import AuthService
from apps.auth.services.cookie import CookieService
from apps.auth.services.jwt import JWTService
from apps.user.container import get_user_service


def get_jwt_service() -> JWTService:
    return JWTService()


def get_cookie_service() -> CookieService:
    return CookieService()


def get_auth_service() -> AuthService:
    cookie_svc = get_cookie_service()
    jwt_svc = get_jwt_service()
    user_svc = get_user_service()
    svc = AuthService(user_svc, cookie_svc, jwt_svc)
    return svc
