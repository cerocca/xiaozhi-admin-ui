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


def get_current_llm_config() -> dict:
    content = read_config_text()
    data = yaml.safe_load(content) or {}

    selected_module = data.get("selected_module", {})
    current_module_name = selected_module.get("llm", "")

    llm_section = data.get("LLM", {})
    current_block = llm_section.get(current_module_name, {}) if current_module_name else {}

    provider_guess = "groq"
    if current_module_name == "openai_llm":
        provider_guess = "openai"
    elif current_module_name == "ollama_llm":
        provider_guess = "ollama"
    elif current_module_name == "anthropic_llm":
        provider_guess = "anthropic"

    return {
        "selected_module_name": current_module_name,
        "selected_block": current_block,
        "provider_guess": provider_guess,
        "raw_config": data,
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
    validation = validate_llm_input(provider, api_key, model, base_url)
    if not validation["ok"]:
        return validation

    preset = PROVIDER_PRESETS[provider]
    module_name = preset["module_name"]

    content = read_config_text()
    data = yaml.safe_load(content) or {}

    if "selected_module" not in data or not isinstance(data["selected_module"], dict):
        data["selected_module"] = {}

    if "LLM" not in data or not isinstance(data["LLM"], dict):
        data["LLM"] = {}

    existing_block = data["LLM"].get(module_name, {})

    final_api_key = existing_block.get("api_key", "")
    if api_key.strip():
        final_api_key = api_key.strip()

    if provider in {"groq", "openai", "anthropic"} and not final_api_key:
        return {
            "ok": False,
            "message": f"API key mancante per provider {provider}",
        }

    data["LLM"][module_name] = {
        "type": preset["type"],
        "base_url": base_url.strip(),
        "api_key": final_api_key,
        "model": model.strip(),
        "temperature": float(temperature),
    }

    data["selected_module"]["llm"] = module_name

    new_yaml = yaml.safe_dump(
        data,
        allow_unicode=True,
        sort_keys=False,
    )

    result = save_config(new_yaml)
    if result.get("ok"):
        result["selected_module_name"] = module_name
        result["provider"] = provider
        result["active_model"] = model.strip()

    return result
