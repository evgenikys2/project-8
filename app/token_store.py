from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional


@dataclass
class TokenData:
    access_token: str
    refresh_token: str
    token_type: str
    expires_at: float
    scope: str

    @property
    def is_expired(self) -> bool:
        return time.time() >= self.expires_at


class TokenStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> Optional[TokenData]:
        if not self.path.exists():
            return None

        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return TokenData(**payload)

    def save(self, token_data: TokenData) -> TokenData:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(asdict(token_data), indent=2), encoding="utf-8")
        return token_data

    def clear(self) -> None:
        if self.path.exists():
            self.path.unlink()

    def save_from_token_response(self, token_payload: dict, existing: Optional[TokenData] = None) -> TokenData:
        expires_in = int(token_payload.get("expires_in", 0))
        token_data = TokenData(
            access_token=token_payload["access_token"],
            refresh_token=token_payload.get("refresh_token") or (existing.refresh_token if existing else ""),
            token_type=token_payload.get("token_type", "Bearer"),
            expires_at=time.time() + max(expires_in, 0),
            scope=token_payload.get("scope", existing.scope if existing else ""),
        )
        return self.save(token_data)
