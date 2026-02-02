from unittest.mock import Mock

from django.test import TestCase

from apps.auth.services.auth import AuthService


class AuthServiceRefreshTokenTest(TestCase):
    def setUp(self) -> None:
        self.user = Mock(id=1)

        self.user_service = Mock()
        self.user_service.get_user_by_id.return_value = self.user

        self.jwt_service = Mock()
        self.jwt_service.decode_token.return_value = Mock(user_id=1)
        self.jwt_service.create_access_token.return_value = "access.jwt"
        self.jwt_service.create_refresh_token.return_value = "refresh.jwt"

        self.auth_service = AuthService(
            user_svc=self.user_service,
            jwt_svc=self.jwt_service,
            email_confierm_svc=Mock(),
        )

    def test_refresh_token_success(self) -> None:
        result = self.auth_service.refresh_token({"refresh_token": "valid.token"})

        self.assertEqual(result["access_token"], "access.jwt")
