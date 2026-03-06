from __future__ import annotations

import logging
import secrets
import time
from contextlib import asynccontextmanager
from typing import Any, Optional

from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse, RedirectResponse

from app.config import get_settings
from app.errors import WhoopAPIError
from app.token_store import TokenStore
from app.whoop_client import WhoopClient


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("whoop_ai_assistant")

settings = get_settings()
token_store = TokenStore(settings.token_store_path)
whoop_client = WhoopClient(settings, token_store)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.oauth_states = set()
    logger.info("WHOOP AI Assistant started")
    yield
    logger.info("WHOOP AI Assistant stopped")


app = FastAPI(title="WHOOP AI Assistant", version="0.1.0", lifespan=lifespan)


def _mask_api_key(api_key: str) -> str:
    if len(api_key) <= 8:
        return "*" * len(api_key)
    return f"{api_key[:4]}...{api_key[-4:]}"


def _build_context_payload(
    profile: dict[str, Any],
    recovery: dict[str, Any],
    sleep: dict[str, Any],
    workouts: dict[str, Any],
) -> dict[str, Any]:
    latest_recovery = (recovery.get("records") or [None])[0]
    latest_sleep = (sleep.get("records") or [None])[0]
    recent_workouts = workouts.get("records") or []
    return {
        "profile": profile,
        "latest_recovery": latest_recovery,
        "latest_sleep": latest_sleep,
        "recent_workouts": recent_workouts[:5],
        "summary": {
            "recovery_score": ((latest_recovery or {}).get("score") or {}).get("recovery_score"),
            "resting_heart_rate": ((latest_recovery or {}).get("score") or {}).get("resting_heart_rate"),
            "hrv_rmssd_milli": ((latest_recovery or {}).get("score") or {}).get("hrv_rmssd_milli"),
            "sleep_performance_percentage": ((latest_sleep or {}).get("score") or {}).get("sleep_performance_percentage"),
            "sleep_efficiency_percentage": ((latest_sleep or {}).get("score") or {}).get("sleep_efficiency_percentage"),
            "recent_workout_count": len(recent_workouts[:5]),
        },
    }


def _build_public_assistant_context(
    recovery: dict[str, Any],
    sleep: dict[str, Any],
    workouts: dict[str, Any],
) -> dict[str, Any]:
    latest_recovery = (recovery.get("records") or [None])[0] or {}
    latest_sleep = (sleep.get("records") or [None])[0] or {}
    recent_workouts = workouts.get("records") or []

    def slim_workout(item: dict[str, Any]) -> dict[str, Any]:
        score = item.get("score") or {}
        return {
            "sport_name": item.get("sport_name"),
            "start": item.get("start"),
            "end": item.get("end"),
            "strain": score.get("strain"),
            "average_heart_rate": score.get("average_heart_rate"),
            "max_heart_rate": score.get("max_heart_rate"),
        }

    recovery_score = latest_recovery.get("score") or {}
    sleep_score = latest_sleep.get("score") or {}
    sleep_stage_summary = sleep_score.get("stage_summary") or {}

    return {
        "readiness": {
            "recovery_score": recovery_score.get("recovery_score"),
            "resting_heart_rate": recovery_score.get("resting_heart_rate"),
            "hrv_rmssd_milli": recovery_score.get("hrv_rmssd_milli"),
            "spo2_percentage": recovery_score.get("spo2_percentage"),
        },
        "sleep": {
            "sleep_performance_percentage": sleep_score.get("sleep_performance_percentage"),
            "sleep_efficiency_percentage": sleep_score.get("sleep_efficiency_percentage"),
            "sleep_consistency_percentage": sleep_score.get("sleep_consistency_percentage"),
            "respiratory_rate": sleep_score.get("respiratory_rate"),
            "total_in_bed_time_milli": sleep_stage_summary.get("total_in_bed_time_milli"),
            "total_awake_time_milli": sleep_stage_summary.get("total_awake_time_milli"),
        },
        "recent_workouts": [slim_workout(item) for item in recent_workouts[:5]],
        "summary": {
            "recent_workout_count": len(recent_workouts[:5]),
            "latest_workout_sport": (recent_workouts[0].get("sport_name") if recent_workouts else None),
        },
    }


def _build_assistant_action_schema() -> dict[str, Any]:
    return {
        "openapi": "3.1.0",
        "info": {
            "title": "WHOOP AI Assistant Action API",
            "version": "1.0.0",
            "description": "Minimal action schema for retrieving current WHOOP health context for one user.",
        },
        "servers": [{"url": settings.app_base_url}],
        "paths": {
            "/health/action": {
                "get": {
                    "operationId": "getActionHealthStatus",
                    "summary": "Get action health",
                    "description": "Returns lightweight status for assistant action debugging.",
                    "responses": {
                        "200": {
                            "description": "Action health status",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {"type": "string"},
                                            "assistant_action_ready": {"type": "boolean"},
                                        },
                                        "required": ["status", "assistant_action_ready"],
                                    }
                                }
                            },
                        }
                    },
                }
            },
            "/health": {
                "get": {
                    "operationId": "getHealthStatus",
                    "summary": "Get service health",
                    "description": "Returns basic service status and whether private endpoint protection is enabled.",
                    "responses": {
                        "200": {
                            "description": "Health status",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {"type": "string"},
                                            "app_base_url": {"type": "string"},
                                            "authorized": {"type": "boolean"},
                                            "api_key_protected": {"type": "boolean"},
                                            "api_key_hint": {"type": ["string", "null"]},
                                        },
                                        "required": ["status", "authorized", "api_key_protected"],
                                    }
                                }
                            },
                        }
                    },
                }
            },
            "/whoop/context": {
                "get": {
                    "operationId": "getWhoopContext",
                    "summary": "Get current WHOOP context",
                    "description": "Returns a compact snapshot of the user's latest WHOOP profile, recovery, sleep, recent workouts, and summary metrics.",
                    "security": [{"ApiKeyAuth": []}],
                    "responses": {
                        "200": {
                            "description": "WHOOP context",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "profile": {"type": "object", "additionalProperties": True},
                                            "latest_recovery": {"type": "object", "additionalProperties": True},
                                            "latest_sleep": {"type": "object", "additionalProperties": True},
                                            "recent_workouts": {
                                                "type": "array",
                                                "items": {"type": "object", "additionalProperties": True},
                                            },
                                            "summary": {
                                                "type": "object",
                                                "properties": {
                                                    "recovery_score": {"type": ["number", "null"]},
                                                    "resting_heart_rate": {"type": ["number", "null"]},
                                                    "hrv_rmssd_milli": {"type": ["number", "null"]},
                                                    "sleep_performance_percentage": {"type": ["number", "null"]},
                                                    "sleep_efficiency_percentage": {"type": ["number", "null"]},
                                                    "recent_workout_count": {"type": "integer"},
                                                },
                                            },
                                        },
                                        "required": [
                                            "profile",
                                            "latest_recovery",
                                            "latest_sleep",
                                            "recent_workouts",
                                            "summary",
                                        ],
                                    }
                                }
                            },
                        },
                        "401": {
                            "description": "Missing or invalid API key",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "error": {"type": "string"},
                                            "hint": {"type": "string"},
                                        },
                                    }
                                }
                            },
                        },
                    },
                }
            },
        },
        "components": {
            "schemas": {},
            "securitySchemes": {
                "ApiKeyAuth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-API-Key",
                    "description": "Private API key for WHOOP-backed assistant access.",
                }
            }
        },
    }


def _build_assistant_public_schema() -> dict[str, Any]:
    return {
        "openapi": "3.1.0",
        "info": {
            "title": "WHOOP AI Assistant Public Action API",
            "version": "1.0.0",
            "description": "Action schema for retrieving a reduced WHOOP context suitable for assistant use.",
        },
        "servers": [{"url": settings.app_base_url}],
        "paths": {
            "/health/action": {
                "get": {
                    "operationId": "getActionHealthStatus",
                    "summary": "Get action health",
                    "description": "Returns lightweight status for assistant action debugging.",
                    "responses": {
                        "200": {
                            "description": "Action health status",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {"type": "string"},
                                            "assistant_action_ready": {"type": "boolean"},
                                        },
                                        "required": ["status", "assistant_action_ready"],
                                    }
                                }
                            },
                        }
                    },
                }
            },
            "/assistant/context": {
                "get": {
                    "operationId": "getAssistantContext",
                    "summary": "Get reduced WHOOP context",
                    "description": "Returns a reduced WHOOP context optimized for assistant reasoning without direct personal identifiers.",
                    "responses": {
                        "200": {
                            "description": "Reduced WHOOP context",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "readiness": {"type": "object", "additionalProperties": True},
                                            "sleep": {"type": "object", "additionalProperties": True},
                                            "recent_workouts": {
                                                "type": "array",
                                                "items": {"type": "object", "additionalProperties": True},
                                            },
                                            "summary": {"type": "object", "additionalProperties": True},
                                        },
                                        "required": ["readiness", "sleep", "recent_workouts", "summary"],
                                    }
                                }
                            },
                        }
                    },
                }
            },
        },
        "components": {"schemas": {}},
    }


@app.middleware("http")
async def log_requests(request: Request, call_next):
    started_at = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - started_at) * 1000
    logger.info("%s %s -> %s (%.2f ms)", request.method, request.url.path, response.status_code, duration_ms)
    return response


@app.middleware("http")
async def protect_private_endpoints(request: Request, call_next):
    protected_paths = ("/whoop/",)
    if not any(request.url.path.startswith(path) for path in protected_paths):
        return await call_next(request)

    if not settings.app_api_key:
        return await call_next(request)

    provided_key = request.headers.get("x-api-key", "")
    if not provided_key:
        provided_key = request.headers.get("api-key", "")
    if not provided_key:
        provided_key = request.headers.get("x-api-key".upper(), "")
    if not provided_key:
        provided_key = request.query_params.get("api_key", "")
    auth_header = request.headers.get("authorization", "")
    if auth_header.lower().startswith("bearer "):
        provided_key = auth_header.split(" ", 1)[1].strip()
    elif auth_header and not provided_key:
        provided_key = auth_header.strip()

    if not provided_key or not secrets.compare_digest(provided_key, settings.app_api_key):
        return JSONResponse(
            status_code=401,
            content={
                "error": "Missing or invalid API key for private WHOOP endpoints.",
                "hint": "Send `X-API-Key: <APP_API_KEY>` or `Authorization: Bearer <APP_API_KEY>`.",
            },
        )

    return await call_next(request)


@app.exception_handler(WhoopAPIError)
async def whoop_api_error_handler(_: Request, exc: WhoopAPIError):
    payload = {
        "error": exc.message,
        "upstream_status": exc.upstream_status,
        "details": exc.details,
    }
    if exc.retry_after:
        payload["retry_after"] = exc.retry_after
    return JSONResponse(status_code=exc.status_code, content=payload)


def _require_oauth_config() -> None:
    missing = []
    if not settings.whoop_client_id:
        missing.append("WHOOP_CLIENT_ID")
    if not settings.whoop_client_secret:
        missing.append("WHOOP_CLIENT_SECRET")
    if not settings.whoop_redirect_uri:
        missing.append("WHOOP_REDIRECT_URI")
    if missing:
        raise WhoopAPIError(
            f"Missing WHOOP configuration: {', '.join(missing)}. Fill in the .env file first.",
            status_code=500,
        )


def _collection_params(
    limit: int,
    start: Optional[str],
    end: Optional[str],
    next_token: Optional[str],
) -> dict[str, object]:
    return {
        "limit": limit,
        "start": start,
        "end": end,
        "nextToken": next_token,
    }


@app.get("/health")
async def health() -> dict[str, object]:
    token_data = token_store.load()
    return {
        "status": "ok",
        "app_base_url": settings.app_base_url,
        "authorized": token_data is not None,
        "api_key_protected": bool(settings.app_api_key),
        "api_key_hint": _mask_api_key(settings.app_api_key) if settings.app_api_key else None,
    }


@app.get("/health/action")
async def action_health() -> dict[str, object]:
    return {
        "status": "ok",
        "assistant_action_ready": True,
    }


@app.get("/openapi/assistant.json")
async def assistant_openapi() -> dict[str, Any]:
    return _build_assistant_action_schema()


@app.get("/openapi/assistant-public.json")
async def assistant_public_openapi() -> dict[str, Any]:
    return _build_assistant_public_schema()


@app.get("/auth/login")
async def auth_login(request: Request):
    _require_oauth_config()
    auth_url, state = whoop_client.build_auth_url()
    request.app.state.oauth_states.add(state)
    return RedirectResponse(url=auth_url, status_code=307)


@app.get("/auth/callback")
async def auth_callback(request: Request, code: str, state: Optional[str] = None) -> dict[str, object]:
    _require_oauth_config()
    if state and state not in request.app.state.oauth_states:
        raise WhoopAPIError("Invalid OAuth state received from WHOOP.", status_code=400)
    if state:
        request.app.state.oauth_states.discard(state)

    token_data = await whoop_client.exchange_code_for_token(code)
    return {
        "message": "WHOOP authorization completed and token saved.",
        "scope": token_data.scope,
        "expires_at": token_data.expires_at,
    }


@app.get("/whoop/profile")
async def whoop_profile() -> dict[str, object]:
    return await whoop_client.get_profile()


@app.get("/whoop/recovery")
async def whoop_recovery(
    limit: int = Query(default=10, ge=1, le=25),
    start: Optional[str] = None,
    end: Optional[str] = None,
    next_token: Optional[str] = Query(default=None, alias="nextToken"),
) -> dict[str, object]:
    return await whoop_client.get_recovery(**_collection_params(limit, start, end, next_token))


@app.get("/whoop/sleep")
async def whoop_sleep(
    limit: int = Query(default=10, ge=1, le=25),
    start: Optional[str] = None,
    end: Optional[str] = None,
    next_token: Optional[str] = Query(default=None, alias="nextToken"),
) -> dict[str, object]:
    return await whoop_client.get_sleep(**_collection_params(limit, start, end, next_token))


@app.get("/whoop/workouts")
async def whoop_workouts(
    limit: int = Query(default=10, ge=1, le=25),
    start: Optional[str] = None,
    end: Optional[str] = None,
    next_token: Optional[str] = Query(default=None, alias="nextToken"),
) -> dict[str, object]:
    return await whoop_client.get_workouts(**_collection_params(limit, start, end, next_token))


@app.get("/whoop/context")
async def whoop_context() -> dict[str, Any]:
    profile = await whoop_client.get_profile()
    recovery = await whoop_client.get_recovery(limit=1)
    sleep = await whoop_client.get_sleep(limit=1)
    workouts = await whoop_client.get_workouts(limit=5)
    return _build_context_payload(profile, recovery, sleep, workouts)


@app.get("/assistant/context")
async def assistant_context() -> dict[str, Any]:
    recovery = await whoop_client.get_recovery(limit=1)
    sleep = await whoop_client.get_sleep(limit=1)
    workouts = await whoop_client.get_workouts(limit=5)
    return _build_public_assistant_context(recovery, sleep, workouts)
