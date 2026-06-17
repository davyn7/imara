# app/activity_logs/middleware.py

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.activity_logs.schemas import ActivityLogBase
from app.activity_logs.db import add_activity_log_db

SKIP_PATH_PREFIXES = ("/docs", "/redoc", "/openapi.json")

def _parse_path(path: str):
    parts = [part for part in path.strip("/").split("/") if part]
    if not parts:
        return None, None
    entity_type = parts[0]
    entity_id = None
    for part in reversed(parts):
        if part.isdigit():
            entity_id = part
            idx = parts.index(part)
            if idx > 0:
                entity_type = parts[idx - 1]
            break
    return entity_type, entity_id

def _should_skip(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in SKIP_PATH_PREFIXES)

class ActivityLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        path = request.url.path
        if _should_skip(path):
            return response
        entity_type, entity_id = _parse_path(path)
        activity_log = ActivityLogBase(
            entity_type=entity_type,
            entity_id=entity_id,
            action=f"{request.method} {path}",
            method=request.method,
            path=path,
            status_code=response.status_code,
        )
        try:
            await add_activity_log_db(activity_log)
        except Exception:
            pass
        return response
