from django.contrib.auth.tokens import default_token_generator

from apps.user.models import User

from .abstructs import TokenGenerator


class DjangoTokenGenerator(TokenGenerator):
    def make(self, user: User) -> str:
        return default_token_generator.make_token(user)

    def check_token(self, user: User, token: str) -> bool:
        return default_token_generator.check_token(user, token)
