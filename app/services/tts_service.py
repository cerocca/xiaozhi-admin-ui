import yaml

from app.services.config_service import read_config_text


def _safe_load_config_data() -> dict:
    try:
        content = read_config_text()
        data = yaml.safe_load(content) or {}
    except (OSError, yaml.YAMLError):
        return {}

    if not isinstance(data, dict):
        return {}
    return data


def _get_dict(data: dict, key: str) -> dict:
    value = data.get(key, {})
    if isinstance(value, dict):
        return value
    return {}


def _guess_provider(profile_name: str, block: dict) -> str:
    block = block if isinstance(block, dict) else {}
    model = str(block.get("model", "") or "").strip().lower()
    api_url = str(block.get("api_url", "") or block.get("base_url", "") or "").strip().lower()

    for key in ("provider", "provider_name", "type"):
        value = str(block.get(key, "") or "").strip()
        if value:
            return value

    if model == "piper" or "8091" in api_url or "piper" in api_url:
        return "piper"

    module_name = str(block.get("module", "") or block.get("module_name", "") or "").strip()
    if module_name:
        return module_name

    return str(profile_name or "").strip()


def _resolve_active_profile_name(data: dict, section_name: str, runtime_key: str, legacy_key: str, logical_key: str) -> str:
    section = _get_dict(data, section_name)
    runtime = _get_dict(data, "runtime")
    selected_module = _get_dict(data, "selected_module")

    runtime_profile = str(runtime.get(runtime_key, "") or "").strip()
    legacy_profile = str(selected_module.get(legacy_key, "") or "").strip()
    logical_profile = str(selected_module.get(logical_key, "") or "").strip()

    for candidate in (runtime_profile, legacy_profile, logical_profile):
        if candidate and isinstance(section.get(candidate), dict):
            return candidate

    for profile_name, block in section.items():
        if isinstance(block, dict):
            return str(profile_name)

    return ""


def get_tts_page_data() -> dict:
    data = _safe_load_config_data()
    tts_section = _get_dict(data, "TTS")
    runtime = _get_dict(data, "runtime")
    selected_module = _get_dict(data, "selected_module")

    active_profile_name = _resolve_active_profile_name(
        data=data,
        section_name="TTS",
        runtime_key="tts_profile",
        legacy_key="tts",
        logical_key="TTS",
    )

    profiles = []
    for profile_name, block in tts_section.items():
        if not isinstance(block, dict):
            continue

        endpoint = str(block.get("api_url", "") or block.get("base_url", "") or "").strip()
        profiles.append(
            {
                "profile_name": str(profile_name),
                "provider": _guess_provider(profile_name, block),
                "type": str(block.get("type", "") or "").strip(),
                "model": str(block.get("model", "") or block.get("model_name", "") or "").strip(),
                "voice": str(block.get("voice", "") or "").strip(),
                "endpoint": endpoint,
                "speed": block.get("speed", ""),
                "is_active": str(profile_name) == active_profile_name,
                "is_local_piper": _guess_provider(profile_name, block) == "piper",
            }
        )

    active = next((profile for profile in profiles if profile["is_active"]), {})

    return {
        "profiles": profiles,
        "active": active,
        "runtime_tts_profile": str(runtime.get("tts_profile", "") or "").strip(),
        "legacy_selected_module_name": str(selected_module.get("tts", "") or "").strip(),
        "logical_selected_module_name": str(selected_module.get("TTS", "") or "").strip(),
    }
