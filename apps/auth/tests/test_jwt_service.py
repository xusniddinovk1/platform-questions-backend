from datetime import datetime, timedelta

import jwt
from django.test import TestCase

from apps.auth.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM, JWT_SECRET
from apps.auth.services.jwt import JWTService
from apps.user.models.user_model import User


class JWTServiceTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
            phone="+998901234567",
        )
        self.jwt_service = JWTService()

    def test_create_access_token_returns_string(self) -> None:
        token = self.jwt_service.create_access_token(self.user.id)
        self.assertIsInstance(token, str)

    def test_access_token_contains_user_id(self) -> None:
        token = self.jwt_service.create_access_token(self.user.id)

        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
        )

        self.assertEqual(payload["user_id"], self.user.id)

    def test_access_token_expiration_time(self) -> None:
        token = self.jwt_service.create_access_token(self.user.id)

        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
        )

        exp = datetime.fromtimestamp(payload["exp"])
        now = datetime.utcnow()

        self.assertTrue(
            now < exp <= now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES + 1)
        )
