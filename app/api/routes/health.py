import httpx
from fastapi import APIRouter, Response, status
from sqlalchemy import text

from app.core.config import get_settings
from app.db.session import engine

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    """Liveness: the API process is up."""
    return {"status": "ok"}


@router.get("/health/ready")
def ready(response: Response) -> dict:
    """Readiness: check connections to Postgres and Ollama."""
    checks: dict[str, str] = {}

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception as exc:  # noqa: BLE001
        checks["database"] = f"error: {exc.__class__.__name__}"

    try:
        r = httpx.get(f"{get_settings().ollama_base_url}/api/tags", timeout=3)
        r.raise_for_status()
        checks["ollama"] = "ok"
    except Exception as exc:  # noqa: BLE001
        checks["ollama"] = f"error: {exc.__class__.__name__}"

    healthy = all(v == "ok" for v in checks.values())
    if not healthy:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {"status": "ok" if healthy else "degraded", "checks": checks}
