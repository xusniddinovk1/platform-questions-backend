import os

ENV = os.getenv("DJANGO_ENV", "dev")

if ENV == "prod":
    from .prod import ALLOWED_HOSTS, CORS_ALLOWED_ORIGINS, DATABASES, DEBUG
else:
    from .dev import ALLOWED_HOSTS, CORS_ALLOWED_ORIGINS, DATABASES, DEBUG

__all__ = ["ALLOWED_HOSTS", "CORS_ALLOWED_ORIGINS", "DATABASES", "DEBUG"]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"config.settings.{ENV}")
