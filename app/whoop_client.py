from __future__ import annotations

import logging
import secrets
import string
import time
from typing import Any, Optional
from urllib.parse import urlencode

import httpx

from app.config import Settings
from app.errors import WhoopAPIError
from app.token_store import TokenData, TokenStore


logger = logging.getLogger("whoop_client")


AUTH_URL = "https://api.prod.whoop.com/oauth/oauth2/auth"
TOKEN_URL = "https://api.prod.whoop.com/oauth/oauth2/token"
API_BASE_URL = "https://api.prod.whoop.com/developer/v2"
STATE_ALPHABET = string.ascii_letters + string.digits


class WhoopClient:
    def __init__(self, settings: Settings, token_store: TokenStore) -> None:
        self.settings = settings
        self.token_store = token_store

    def build_auth_url(self, state: Optional[str] = None) -> tuple[str, str]:
        oauth_state = state or "".join(secrets.choice(STATE_ALPHABET) for _ in range(8))
        params = {
            "client_id": self.settings.whoop_client_id,
            "redirect_uri": self.settings.whoop_redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.settings.scope_list),
            "state": oauth_state,
        }
        return f"{AUTH_URL}?{urlencode(params)}", oauth_state

    async def exchange_code_for_token(self, code: str) -> TokenData:
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.settings.whoop_client_id,
            "client_secret": self.settings.whoop_client_secret,
            "redirect_uri": self.settings.whoop_redirect_uri,
        }
        logger.info("Exchanging WHOOP authorization code for token")
        token_payload = await self._post_token(payload)
        return self.token_store.save_from_token_response(token_payload)

    async def refresh_access_token(self) -> TokenData:
        token_data = self.token_store.load()
        if not token_data or not token_data.refresh_token:
            raise WhoopAPIError(
                "WHOOP token is missing or cannot be refreshed. Re-run /auth/login.",
                status_code=401,
            )

        payload = {
            "grant_type": "refresh_token",
            "refresh_token": token_data.refresh_token,
            "client_id": self.settings.whoop_client_id,
            "client_secret": self.settings.whoop_client_secret,
        }
        logger.info("Refreshing WHOOP access token")
        token_payload = await self._post_token(payload)
        return self.token_store.save_from_token_response(token_payload, existing=token_data)

    async def get_profile(self) -> dict[str, Any]:
        return await self._api_get("/user/profile/basic")

    async def get_recovery(self, **params: Any) -> dict[str, Any]:
        return await self._api_get("/recovery", params=self._clean_params(params))

    async def get_sleep(self, **params: Any) -> dict[str, Any]:
        return await self._api_get("/activity/sleep", params=self._clean_params(params))

    async def get_workouts(self, **params: Any) -> dict[str, Any]:
        return await self._api_get("/activity/workout", params=self._clean_params(params))

    async def _api_get(
        self,
        path: str,
        *,
        params: Optional[dict[str, Any]] = None,
        retry_after_refresh: bool = True,
    ) -> dict[str, Any]:
        access_token = await self._ensure_valid_access_token()
        url = f"{API_BASE_URL}{path}"
        headers = {"Authorization": f"Bearer {access_token}"}

        async with httpx.AsyncClient(timeout=20.0) as client:
            logger.info("WHOOP GET %s params=%s", path, params)
            response = await client.get(url, headers=headers, params=params)

        if response.status_code == 401 and retry_after_refresh:
            logger.warning("WHOOP returned 401 for %s, attempting token refresh", path)
            await self.refresh_access_token()
            return await self._api_get(path, params=params, retry_after_refresh=False)

        return self._handle_response(response)

    async def _ensure_valid_access_token(self) -> str:
        token_data = self.token_store.load()
        if not token_data:
            raise WhoopAPIError(
                "WHOOP is not authorized yet. Open /auth/login first.",
                status_code=401,
            )

        # Refresh slightly before expiry to avoid race conditions on live requests.
        if token_data.expires_at - time.time() <= 60:
            token_data = await self.refresh_access_token()

        return token_data.access_token

    async def _post_token(self, payload: dict[str, str]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(
                TOKEN_URL,
                data=payload,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
        return self._handle_response(response)

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        parsed = self._parse_json(response)
        if response.is_success:
            return parsed

        details = parsed or response.text or None
        upstream_status = response.status_code

        if upstream_status == 401:
            raise WhoopAPIError(
                "WHOOP authorization failed or expired. Re-run /auth/login.",
                status_code=401,
                upstream_status=upstream_status,
                details=details,
            )
        if upstream_status == 429:
            raise WhoopAPIError(
                "WHOOP API rate limit exceeded. Wait a bit and retry.",
                status_code=429,
                upstream_status=upstream_status,
                retry_after=response.headers.get("Retry-After"),
                details=details,
            )
        if upstream_status >= 500:
            raise WhoopAPIError(
                "WHOOP API is temporarily unavailable. Try again later.",
                status_code=502,
                upstream_status=upstream_status,
                details=details,
            )

        raise WhoopAPIError(
            "WHOOP API request failed.",
            status_code=400 if upstream_status < 500 else 502,
            upstream_status=upstream_status,
            details=details,
        )

    @staticmethod
    def _parse_json(response: httpx.Response) -> dict[str, Any]:
        try:
            payload = response.json()
            return payload if isinstance(payload, dict) else {"data": payload}
        except ValueError:
            return {}

    @staticmethod
    def _clean_params(params: dict[str, Any]) -> dict[str, Any]:
        return {key: value for key, value in params.items() if value is not None}
