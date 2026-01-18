from typing import Dict, cast

from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view


class JWTSchemGenerator(OpenAPISchemaGenerator):  # type: ignore[misc]
    def get_security_definitions(self) -> Dict[str, Dict[str, str]]:
        security_definitions = cast(
            Dict[str, Dict[str, str]], super().get_security_definitions()
        )

        security_definitions["Bearer"] = {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
        }
        return security_definitions


schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version="v1",
        description="Questions-Answers API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    generator_class=JWTSchemGenerator,
)
