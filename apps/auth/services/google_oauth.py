import secrets
from datetime import datetime, timedelta
from typing import Any
from urllib.parse import urlencode

import jwt
import requests

from apps.auth.config import (
    GOOGLE_AUTH_ENDPOINT,
    GOOGLE_CERTS_ENDPOINT,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_ISSUERS,
    GOOGLE_REDIRECT_URI,
    GOOGLE_TOKEN_ENDPOINT,
    JWT_SECRET,
    OAUTH_STATE_EXPIRE_MINUTES,
)
from apps.auth.dto.google_oauth import GoogleUserInfoDTO


class GoogleOAuthService:
    """Handles Google OAuth 2.0 / OpenID Connect flow."""

    def __init__(
        self,
        client_id: str = GOOGLE_CLIENT_ID,
        client_secret: str = GOOGLE_CLIENT_SECRET,
        redirect_uri: str = GOOGLE_REDIRECT_URI,
    ) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri

    # ── State / CSRF ──────────────────────────────────────────────

    def generate_state_token(self) -> str:
        """Signed JWT used as the OAuth *state* parameter (CSRF protection)."""
        payload = {
            "nonce": secrets.token_urlsafe(32),
            "exp": datetime.utcnow() + timedelta(minutes=OAUTH_STATE_EXPIRE_MINUTES),
            "iat": datetime.utcnow(),
            "purpose": "google_oauth_state",
        }
        return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    @staticmethod
    def verify_state_token(state: str) -> bool:
        """Return *True* only when *state* is a valid, non-expired token."""
        try:
            payload: dict[str, Any] = jwt.decode(state, JWT_SECRET, algorithms=["HS256"])
            return payload.get("purpose") == "google_oauth_state"
        except (jwt.ExpiredSignatureError, jwt.DecodeError):
            return False

    # ── Authorization URL ─────────────────────────────────────────

    def build_authorization_url(self, state: str) -> str:
        params = {
            "client_id": self._client_id,
            "redirect_uri": self._redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "state": state,
            "prompt": "consent",
        }
        return f"{GOOGLE_AUTH_ENDPOINT}?{urlencode(params)}"

    # ── Token exchange ────────────────────────────────────────────

    def exchange_code(self, code: str) -> dict[str, Any]:
        """Exchange the authorization *code* for Google tokens."""
        resp = requests.post(
            GOOGLE_TOKEN_ENDPOINT,
            data={
                "code": code,
                "client_id": self._client_id,
                "client_secret": self._client_secret,
                "redirect_uri": self._redirect_uri,
                "grant_type": "authorization_code",
            },
            timeout=10,
        )
        if resp.status_code != 200:
            raise ValueError(f"Google token exchange failed: {resp.text}")
        return resp.json()

    # ── ID-token verification ─────────────────────────────────────

    @staticmethod
    def _fetch_google_jwks() -> dict[str, Any]:
        resp = requests.get(GOOGLE_CERTS_ENDPOINT, timeout=10)
        if resp.status_code != 200:
            raise ValueError("Failed to fetch Google JWKS")
        return resp.json()

    def verify_id_token(self, id_token: str) -> GoogleUserInfoDTO:
        """Verify the ID-token signature and claims, return user info."""
        jwks = self._fetch_google_jwks()

        header = jwt.get_unverified_header(id_token)
        kid: str | None = header.get("kid")

        matching_key: dict[str, Any] | None = next(
            (k for k in jwks.get("keys", []) if k.get("kid") == kid),
            None,
        )
        if matching_key is None:
            raise ValueError("No matching Google signing key found")

        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(matching_key)

        payload: dict[str, Any] = jwt.decode(
            id_token,
            public_key,  # type: ignore[arg-type]
            algorithms=["RS256"],
            audience=self._client_id,
            options={"verify_iss": False},
        )

        iss = payload.get("iss", "")
        if iss not in GOOGLE_ISSUERS:
            raise ValueError(f"Invalid issuer: {iss}")

        return GoogleUserInfoDTO(
            sub=payload["sub"],
            email=payload.get("email", ""),
            email_verified=payload.get("email_verified", False),
            given_name=payload.get("given_name", ""),
            family_name=payload.get("family_name", ""),
            picture=payload.get("picture", ""),
        )

    # ── Public high-level helper ──────────────────────────────────

    def authenticate(self, code: str) -> GoogleUserInfoDTO:
        """Full flow: exchange the authorization code → verify ID-token."""
        tokens = self.exchange_code(code)
        raw_id_token: str | None = tokens.get("id_token")
        if not raw_id_token:
            raise ValueError("No id_token in Google response")
        return self.verify_id_token(raw_id_token)
