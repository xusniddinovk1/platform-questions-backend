import os

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", f"config.settings.{os.getenv('DJANGO_ENV', 'dev')}"
)

application = get_wsgi_application()
