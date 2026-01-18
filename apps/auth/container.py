from .services.cookie_service import CookieService
from .services.jwt_service import JWTService


def get_jwt_service() -> JWTService:
    return JWTService()


def get_cookie_service() -> CookieService:
    return CookieService()
