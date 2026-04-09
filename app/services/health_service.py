import httpx

from app.config import settings

HEALTH_URL = f"http://{settings.backend_host}:{settings.backend_health_port}/api/health"
HEALTH_FALLBACK = {
    "llm": "error",
    "asr": "error",
    "tts": "error",
    "device": "disconnected",
}


def _normalize_health_payload(payload) -> dict:
    if not isinstance(payload, dict):
        return dict(HEALTH_FALLBACK)

    normalized = dict(HEALTH_FALLBACK)
    allowed = {
        "llm": {"ok", "error"},
        "asr": {"ok", "error"},
        "tts": {"ok", "error"},
        "device": {"connected", "disconnected"},
    }

    for key, values in allowed.items():
        value = str(payload.get(key, "") or "").strip().lower()
        if value in values:
            normalized[key] = value

    return normalized


def get_health_status() -> dict:
    try:
        with httpx.Client(timeout=2.5) as client:
            response = client.get(HEALTH_URL)
            response.raise_for_status()
            return _normalize_health_payload(response.json())
    except Exception:
        return dict(HEALTH_FALLBACK)
