from ipaddress import ip_address
from urllib.parse import urlparse

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.services.asr_service import get_active_asr
from app.services.llm_service import get_active_llm
from app.services.status_service import get_dashboard_status
from app.services.tts_service import get_active_tts

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def _build_ui_badges(slug: str) -> list[dict]:
    def _status_badge(label: str, kind: str) -> dict:
        return {"label": label, "kind": kind}

    def _classify_endpoint_scope(endpoint: str, hints=None):
        normalized_endpoint = str(endpoint or "").strip().lower()
        if not normalized_endpoint:
            return None

        for hint in (hints or []):
            if hint and hint.lower() in normalized_endpoint:
                return _status_badge("LOCALE", "info")

        parsed = urlparse(normalized_endpoint)
        hostname = str(parsed.hostname or "").strip().lower()
        if not hostname:
            return None
        if hostname in {"localhost", "127.0.0.1"}:
            return _status_badge("LOCALE", "info")
        try:
            if ip_address(hostname).is_private:
                return _status_badge("LOCALE", "info")
            return _status_badge("REMOTO", "muted")
        except ValueError:
            return _status_badge("REMOTO", "muted")

    if slug == "llm":
        active = get_active_llm()
        badges = []
        profile_name = str(active.get("profile_name", "") or "").strip()
        model = str(active.get("model", "") or "").strip()
        endpoint = str(active.get("base_url", "") or "").strip()

        if not profile_name or not model or not endpoint:
            badges.append(_status_badge("ERR", "err"))
        elif active.get("requires_api_key") and not active.get("has_api_key"):
            badges.append(_status_badge("PARZIALE", "warn"))
        else:
            badges.append(_status_badge("OK", "ok"))

        scope_badge = _classify_endpoint_scope(
            endpoint,
            hints=[str(active.get("provider_id", "") or "").strip(), "11434", "ollama"],
        )
        if scope_badge:
            badges.append(scope_badge)
        if active.get("is_legacy"):
            badges.append(_status_badge("LEGACY", "warn"))
        return badges

    if slug == "asr":
        active = get_active_asr()
        badges = []
        profile_name = str(active.get("profile_name", "") or "").strip()
        model = str(active.get("model", "") or "").strip()
        endpoint = str(active.get("endpoint", "") or "").strip()

        if not profile_name or not model or not endpoint:
            badges.append(_status_badge("ERR", "err"))
        elif active.get("requires_api_key") and not active.get("has_api_key"):
            badges.append(_status_badge("PARZIALE", "warn"))
        else:
            badges.append(_status_badge("OK", "ok"))

        scope_badge = _classify_endpoint_scope(endpoint)
        if scope_badge:
            badges.append(scope_badge)
        return badges

    if slug == "tts":
        active = get_active_tts()
        badges = []
        profile_name = str(active.get("profile_name", "") or "").strip()
        model = str(active.get("model", "") or "").strip()
        endpoint = str(active.get("endpoint", "") or "").strip()

        if not profile_name or not model or not endpoint:
            badges.append(_status_badge("ERR", "err"))
        elif active.get("requires_api_key") and not active.get("has_api_key"):
            badges.append(_status_badge("PARZIALE", "warn"))
        else:
            badges.append(_status_badge("OK", "ok"))

        if active.get("is_local_piper"):
            badges.append(_status_badge("LOCALE", "info"))
            badges.append(_status_badge("PIPER", "info"))
        else:
            scope_badge = _classify_endpoint_scope(endpoint)
            if scope_badge:
                badges.append(scope_badge)
        return badges

    return []


@router.get("/")
def dashboard(request: Request):
    data = get_dashboard_status()
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "request": request,
            "status": data,
            "page_title": "Xiaozhi Admin UI",
        },
    )


@router.get("/ai")
def ai_stack_index(request: Request):
    ui_items = [
        {
            "title": "LLM",
            "href": "/llm",
            "slug": "llm",
            "description": "Generazione delle risposte (modello e profili)",
            "active_profile": str(get_active_llm().get("profile_name", "") or "").strip(),
            "badges": _build_ui_badges("llm"),
        },
        {
            "title": "ASR",
            "href": "/asr",
            "slug": "asr",
            "description": "Speech -> text (riconoscimento vocale)",
            "active_profile": str(get_active_asr().get("profile_name", "") or "").strip(),
            "badges": _build_ui_badges("asr"),
        },
        {
            "title": "TTS",
            "href": "/tts",
            "slug": "tts",
            "description": "Text -> speech (sintesi vocale)",
            "active_profile": str(get_active_tts().get("profile_name", "") or "").strip(),
            "badges": _build_ui_badges("tts"),
        },
    ]
    readonly_items = [
        {
            "title": "VAD",
            "href": "/vad",
            "slug": "vad",
            "description": "Rilevamento presenza voce",
            "badges": [
                {"label": "READ-ONLY", "kind": "muted"},
                {"label": "YAML", "kind": "info"},
            ],
        },
        {
            "title": "Intent",
            "href": "/intent",
            "slug": "intent",
            "description": "Interpretazione della richiesta",
            "badges": [
                {"label": "READ-ONLY", "kind": "muted"},
                {"label": "YAML", "kind": "info"},
            ],
        },
        {
            "title": "Memory",
            "href": "/memory",
            "slug": "memory",
            "description": "Gestione contesto e memoria",
            "badges": [
                {"label": "READ-ONLY", "kind": "muted"},
                {"label": "YAML", "kind": "info"},
            ],
        },
    ]
    return templates.TemplateResponse(
        request,
        "ai_index.html",
        {
            "request": request,
            "page_title": "AI Stack",
            "ui_items": ui_items,
            "readonly_items": readonly_items,
        },
    )
