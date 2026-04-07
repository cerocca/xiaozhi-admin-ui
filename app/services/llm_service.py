import yaml

from app.services.config_service import read_config_text, save_config


PROVIDER_PRESETS = {
    "groq": {
        "module_name": "groq_llm",
        "type": "openai",
        "base_url": "https://api.groq.com/openai/v1",
        "default_model": "llama-3.1-8b-instant",
        "default_api_key": "",
        "default_temperature": 0.7,
        "models": [
            "llama-3.1-8b-instant",
            "llama-3.1-70b-versatile",
        ],
    },
    "openai": {
        "module_name": "openai_llm",
        "type": "openai",
        "base_url": "https://api.openai.com/v1",
        "default_model": "gpt-4o-mini",
        "default_api_key": "",
        "default_temperature": 0.7,
        "models": [
            "gpt-4o-mini",
            "gpt-4.1-mini",
        ],
    },
    "ollama": {
        "module_name": "ollama_llm",
        "type": "openai",
        "base_url": "http://192.168.1.69:11434/v1",
        "default_model": "llama3.1:8b",
        "default_api_key": "not-needed",
        "default_temperature": 0.7,
        "models": [
            "llama3.1:8b",
            "qwen2.5:7b",
        ],
    },
    "anthropic": {
        "module_name": "anthropic_llm",
        "type": "openai",
        "base_url": "https://api.anthropic.com/v1/",
        "default_model": "claude-sonnet-4-20250514",
        "default_api_key": "",
        "default_temperature": 0.7,
        "models": [
            "claude-sonnet-4-20250514",
            "claude-3-5-sonnet-20241022",
        ],
    },
}


def get_provider_presets() -> dict:
    return PROVIDER_PRESETS


def normalize_llm_form_data(
    provider: str,
    api_key: str,
    model: str,
    base_url: str,
    temperature: float,
) -> dict:
    return {
        "provider": str(provider or "").strip(),
        "api_key": str(api_key or "").strip(),
        "model": str(model or "").strip(),
        "base_url": str(base_url or "").strip(),
        "temperature": max(0.0, min(2.0, float(temperature))),
    }


def _safe_load_config_data() -> dict:
    try:
        content = read_config_text()
        data = yaml.safe_load(content) or {}
    except (OSError, yaml.YAMLError):
        return {}

    if not isinstance(data, dict):
        return {}
    return data


def _load_config_data_for_update() -> tuple[dict | None, str]:
    try:
        content = read_config_text()
    except OSError as e:
        return None, f"Impossibile leggere la config corrente: {e}"

    try:
        data = yaml.safe_load(content) or {}
    except yaml.YAMLError as e:
        return None, f"Config corrente non valida: {e}"

    if not isinstance(data, dict):
        return None, "Config corrente non valida: la root YAML deve essere una mappa"

    return data, ""


def _get_dict(data: dict, key: str) -> dict:
    value = data.get(key, {})
    if isinstance(value, dict):
        return value
    return {}


def _provider_from_module_name(module_name: str) -> str:
    if module_name in PROVIDER_PRESETS:
        return module_name

    for provider_name, preset in PROVIDER_PRESETS.items():
        if preset["module_name"] == module_name:
            return provider_name

    return ""


def _guess_provider(module_name: str, block: dict) -> str:
    provider_name = _provider_from_module_name(module_name)
    if provider_name:
        return provider_name

    if not isinstance(block, dict):
        block = {}

    block_base_url = str(block.get("base_url", "")).strip().rstrip("/")
    for preset_provider, preset in PROVIDER_PRESETS.items():
        preset_base_url = str(preset.get("base_url", "")).strip().rstrip("/")
        if block_base_url and block_base_url == preset_base_url:
            return preset_provider

    if "groq" in PROVIDER_PRESETS:
        return "groq"
    return next(iter(PROVIDER_PRESETS), "")


def _get_llm_profile_names(data: dict) -> tuple[str, str]:
    runtime = _get_dict(data, "runtime")
    selected_module = _get_dict(data, "selected_module")

    runtime_llm_profile = str(runtime.get("llm_profile", "") or "").strip()
    legacy_module_name = str(selected_module.get("llm", "") or "").strip()

    return runtime_llm_profile, legacy_module_name


def _get_existing_llm_block(data: dict, *names: str) -> tuple[str, dict]:
    llm_section = _get_dict(data, "LLM")

    for name in names:
        if name and isinstance(llm_section.get(name), dict):
            return name, llm_section[name]

    return "", {}


def get_current_llm_config() -> dict:
    data = _safe_load_config_data()
    runtime_llm_profile, legacy_module_name = _get_llm_profile_names(data)

    current_module_name, current_block = _get_existing_llm_block(
        data,
        runtime_llm_profile,
        legacy_module_name,
    )

    if not current_module_name:
        current_module_name = runtime_llm_profile or legacy_module_name

    provider_guess = _guess_provider(current_module_name, current_block)

    return {
        "selected_module_name": current_module_name,
        "selected_block": current_block,
        "provider_guess": provider_guess,
        "runtime_llm_profile": runtime_llm_profile,
        "legacy_selected_module_name": legacy_module_name,
        "raw_config": data,
    }


def get_llm_form_data() -> dict:
    current = get_current_llm_config()
    presets = get_provider_presets()

    provider_guess = current.get("provider_guess", "groq")
    if provider_guess in presets:
        provider = provider_guess
    elif "groq" in presets:
        provider = "groq"
    else:
        provider = next(iter(presets), "")

    selected_block = current.get("selected_block", {})
    if not isinstance(selected_block, dict):
        selected_block = {}
    preset = presets.get(provider, {})

    return {
        "presets": presets,
        "provider": provider,
        "api_key": selected_block.get("api_key", preset.get("default_api_key", "")),
        "model": selected_block.get("model", preset.get("default_model", "")),
        "base_url": selected_block.get("base_url", preset.get("base_url", "")),
        "temperature": selected_block.get("temperature", preset.get("default_temperature", 0.0)),
        "selected_module_name": current.get("selected_module_name", ""),
    }


def validate_llm_input(provider: str, api_key: str, model: str, base_url: str) -> dict:
    if provider not in PROVIDER_PRESETS:
        return {"ok": False, "message": f"Provider non supportato: {provider}"}

    if not model.strip():
        return {"ok": False, "message": "Il model non può essere vuoto"}

    if not base_url.strip():
        return {"ok": False, "message": "La base URL non può essere vuota"}

    if provider in {"groq", "openai", "anthropic"} and not api_key.strip():
        # Non errore bloccante se la chiave esiste già in config; questo viene gestito dopo.
        return {"ok": True, "message": "ok"}

    return {"ok": True, "message": "ok"}


def update_llm_config(
    provider: str,
    api_key: str,
    model: str,
    base_url: str,
    temperature: float,
) -> dict:
    normalized = normalize_llm_form_data(
        provider,
        api_key,
        model,
        base_url,
        temperature,
    )
    provider = normalized["provider"]
    api_key = normalized["api_key"]
    model = normalized["model"]
    base_url = normalized["base_url"]
    temperature = normalized["temperature"]

    validation = validate_llm_input(provider, api_key, model, base_url)
    if not validation["ok"]:
        return validation

    preset = PROVIDER_PRESETS[provider]
    module_name = preset["module_name"]

    data, load_error = _load_config_data_for_update()
    if load_error:
        return {"ok": False, "message": load_error}

    runtime_llm_profile, legacy_module_name = _get_llm_profile_names(data)

    if "runtime" not in data or not isinstance(data["runtime"], dict):
        data["runtime"] = {}

    if "LLM" not in data or not isinstance(data["LLM"], dict):
        data["LLM"] = {}

    existing_name, existing_block = _get_existing_llm_block(
        data,
        module_name,
        runtime_llm_profile,
        legacy_module_name,
    )
    if not existing_name:
        existing_name = module_name

    final_api_key = existing_block.get("api_key", "")
    if api_key.strip():
        final_api_key = api_key.strip()

    if provider in {"groq", "openai", "anthropic"} and not final_api_key:
        return {
            "ok": False,
            "message": f"API key mancante per provider {provider}",
        }

    updated_block = {}
    if isinstance(existing_block, dict):
        updated_block.update(existing_block)
    updated_block.update(
        {
            "type": preset["type"],
            "base_url": base_url,
            "api_key": final_api_key,
            "model": model,
            "temperature": temperature,
        }
    )

    if existing_name and existing_name != module_name and existing_name in data["LLM"]:
        old_block = data["LLM"].get(existing_name)
        if old_block == existing_block:
            del data["LLM"][existing_name]

    data["LLM"][module_name] = updated_block
    data["runtime"]["llm_profile"] = module_name

    selected_module = data.get("selected_module")
    if isinstance(selected_module, dict):
        selected_module["llm"] = module_name

    new_yaml = yaml.safe_dump(
        data,
        allow_unicode=True,
        sort_keys=False,
    )

    result = save_config(new_yaml)
    if result.get("ok"):
        result["selected_module_name"] = module_name
        result["runtime_llm_profile"] = module_name
        result["legacy_selected_module_name"] = (
            module_name if isinstance(data.get("selected_module"), dict) else ""
        )
        result["provider"] = provider
        result["active_model"] = model
        result["active_base_url"] = base_url

    return result
