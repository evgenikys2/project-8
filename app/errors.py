from __future__ import annotations

from typing import Any, Optional, Union


class WhoopAPIError(Exception):
    def __init__(
        self,
        message: str,
        *,
        status_code: int = 502,
        upstream_status: Optional[int] = None,
        retry_after: Optional[str] = None,
        details: Optional[Union[dict[str, Any], str]] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.upstream_status = upstream_status
        self.retry_after = retry_after
        self.details = details
