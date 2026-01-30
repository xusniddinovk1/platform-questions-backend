from .base import *
from .base import env
import os
import dj_database_url
DEBUG = False
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["platform-questions-backend.com"])

# PostgreSQL из env
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": env("POSTGRES_DB"),
#         "USER": env("POSTGRES_USER"),
#         "PASSWORD": env("POSTGRES_PASSWORD"),
#         "HOST": env("POSTGRES_HOST"),
#         "PORT": env("POSTGRES_PORT", default=5432),
#     }
# }

DATABASES = {
    "default": dj_database_url.parse(
        os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )
}

# CORS для прод
CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS", default=["https://platform-questions-fronted.vercel.app"]
)
