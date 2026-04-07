from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates

from app.services.command_service import run_command
from app.services.llm_service import (
    get_llm_form_data,
    normalize_llm_form_data,
    update_llm_config,
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def _render_llm_page(
    request: Request,
    presets,
    provider,
    api_key,
    model,
    base_url,
    temperature,
    result,
    selected_module_name="",
    active_provider="",
    active_model="",
    active_selected_module_name="",
):
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
            "selected_module_name": selected_module_name,
            "active_provider": active_provider,
            "active_model": active_model,
            "active_selected_module_name": active_selected_module_name,
        },
    )


def _save_llm(
    request: Request,
    provider: str,
    api_key: str,
    model: str,
    base_url: str,
    temperature: float,
    restart=False,
):
    form_data = normalize_llm_form_data(
        provider,
        api_key,
        model,
        base_url,
        temperature,
    )

    result = update_llm_config(
        provider=form_data["provider"],
        api_key=form_data["api_key"],
        model=form_data["model"],
        base_url=form_data["base_url"],
        temperature=form_data["temperature"],
    )

    if restart and result.get("ok"):
        restart_result = run_command(
            ["/home/ciru/xiaozhi-admin-ui/scripts/xserver.sh", "restart"],
            timeout=30,
        )
        result["restart_result"] = restart_result
        if restart_result.get("ok"):
            result["message"] = f'{result["message"]} + restart Xiaozhi completato'
        else:
            result["message"] = f'{result["message"]} ma restart Xiaozhi fallito'

    persisted_state = get_llm_form_data()

    return _render_llm_page(
        request,
        persisted_state.get("presets", {}),
        form_data["provider"],
        form_data["api_key"],
        form_data["model"],
        form_data["base_url"],
        form_data["temperature"],
        result,
        result.get("selected_module_name", persisted_state.get("selected_module_name", "")),
        active_provider=persisted_state.get("provider", ""),
        active_model=persisted_state.get("model", ""),
        active_selected_module_name=persisted_state.get("selected_module_name", ""),
    )


@router.get("/llm")
def llm_page(request: Request):
    form_data = get_llm_form_data()

    return _render_llm_page(
        request,
        form_data["presets"],
        form_data["provider"],
        form_data["api_key"],
        form_data["model"],
        form_data["base_url"],
        form_data["temperature"],
        None,
        form_data["selected_module_name"],
        active_provider=form_data["provider"],
        active_model=form_data["model"],
        active_selected_module_name=form_data["selected_module_name"],
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
    return _save_llm(
        request,
        provider,
        api_key,
        model,
        base_url,
        temperature,
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
    return _save_llm(
        request,
        provider,
        api_key,
        model,
        base_url,
        temperature,
        restart=True,
    )
