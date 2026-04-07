from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates

from app.services.command_service import run_command
from app.services.llm_service import (
    get_current_llm_config,
    get_provider_presets,
    update_llm_config,
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/llm")
def llm_page(request: Request):
    current = get_current_llm_config()
    presets = get_provider_presets()

    provider_guess = current.get("provider_guess", "groq")
    selected_block = current.get("selected_block", {})
    preset = presets[provider_guess]

    return templates.TemplateResponse(
        request,
        "llm.html",
        {
            "request": request,
            "page_title": "LLM Config",
            "presets": presets,
            "provider": provider_guess,
            "api_key": selected_block.get("api_key", preset["default_api_key"]),
            "model": selected_block.get("model", preset["default_model"]),
            "base_url": selected_block.get("base_url", preset["base_url"]),
            "temperature": selected_block.get("temperature", preset["default_temperature"]),
            "result": None,
            "selected_module_name": current.get("selected_module_name", ""),
        },
    )


@router.post("/llm/save")
def llm_save(
    request: Request,
    provider: str = Form(...),
    api_key: str = Form(...),
    model: str = Form(...),
    base_url: str = Form(...),
    temperature: float = Form(...),
):
    presets = get_provider_presets()
    result = update_llm_config(
        provider=provider,
        api_key=api_key,
        model=model,
        base_url=base_url,
        temperature=temperature,
    )

    return templates.TemplateResponse(
        request,
        "llm.html",
        {
            "request": request,
            "page_title": "LLM Config",
            "presets": presets,
            "provider": provider,
            "api_key": api_key,
            "model": model,
            "base_url": base_url,
            "temperature": temperature,
            "result": result,
            "selected_module_name": result.get("selected_module_name", ""),
        },
    )


@router.post("/llm/save-and-restart")
def llm_save_and_restart(
    request: Request,
    provider: str = Form(...),
    api_key: str = Form(...),
    model: str = Form(...),
    base_url: str = Form(...),
    temperature: float = Form(...),
):
    presets = get_provider_presets()

    result = update_llm_config(
        provider=provider,
        api_key=api_key,
        model=model,
        base_url=base_url,
        temperature=temperature,
    )

    if result.get("ok"):
        restart_result = run_command(
            ["/home/ciru/xiaozhi-admin-ui/scripts/xserver.sh", "restart"],
            timeout=30,
        )
        result["restart_result"] = restart_result
        if restart_result.get("ok"):
            result["message"] = f'{result["message"]} + restart Xiaozhi completato'
        else:
            result["message"] = f'{result["message"]} ma restart Xiaozhi fallito'

    return templates.TemplateResponse(
        request,
        "llm.html",
        {
            "request": request,
            "page_title": "LLM Config",
            "presets": presets,
            "provider": provider,
            "api_key": api_key,
            "model": model,
            "base_url": base_url,
            "temperature": temperature,
            "result": result,
            "selected_module_name": result.get("selected_module_name", ""),
        },
    )
