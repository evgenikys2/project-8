from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    whoop_client_id: str = Field(default="", alias="WHOOP_CLIENT_ID")
    whoop_client_secret: str = Field(default="", alias="WHOOP_CLIENT_SECRET")
    whoop_redirect_uri: str = Field(default="http://localhost:8000/auth/callback", alias="WHOOP_REDIRECT_URI")
    whoop_scopes: str = Field(
        default="offline read:profile read:recovery read:sleep read:workout",
        alias="WHOOP_SCOPES",
    )
    app_base_url: str = Field(default="http://localhost:8000", alias="APP_BASE_URL")
    app_api_key: str = Field(default="", alias="APP_API_KEY")

    @property
    def scope_list(self) -> list[str]:
        return [scope for scope in self.whoop_scopes.split() if scope]

    @property
    def token_store_path(self) -> Path:
        return PROJECT_ROOT / "data" / "whoop_tokens.json"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
