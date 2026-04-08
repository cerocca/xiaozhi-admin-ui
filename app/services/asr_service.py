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


def _get_model(block: dict) -> str:
    if not isinstance(block, dict):
        return ""
    for key in ("model", "model_name"):
        value = str(block.get(key, "") or "").strip()
        if value:
            return value
    return ""


def _guess_provider(profile_name: str, block: dict) -> str:
    block = block if isinstance(block, dict) else {}

    for key in ("provider", "provider_name", "type"):
        value = str(block.get(key, "") or "").strip()
        if value:
            return value

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


def get_asr_page_data() -> dict:
    data = _safe_load_config_data()
    asr_section = _get_dict(data, "ASR")
    runtime = _get_dict(data, "runtime")
    selected_module = _get_dict(data, "selected_module")

    active_profile_name = _resolve_active_profile_name(
        data=data,
        section_name="ASR",
        runtime_key="asr_profile",
        legacy_key="asr",
        logical_key="ASR",
    )

    profiles = []
    for profile_name, block in asr_section.items():
        if not isinstance(block, dict):
            continue

        profiles.append(
            {
                "profile_name": str(profile_name),
                "provider": _guess_provider(profile_name, block),
                "type": str(block.get("type", "") or "").strip(),
                "model": _get_model(block),
                "base_url": str(block.get("base_url", "") or "").strip(),
                "is_active": str(profile_name) == active_profile_name,
            }
        )

    active = next((profile for profile in profiles if profile["is_active"]), {})

    return {
        "profiles": profiles,
        "active": active,
        "runtime_asr_profile": str(runtime.get("asr_profile", "") or "").strip(),
        "legacy_selected_module_name": str(selected_module.get("asr", "") or "").strip(),
        "logical_selected_module_name": str(selected_module.get("ASR", "") or "").strip(),
    }
