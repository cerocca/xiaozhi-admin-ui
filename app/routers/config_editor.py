from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates

from app.services.config_service import (
    read_config_text,
    save_config,
    validate_yaml_text,
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/config")
def config_page(request: Request):
    content = read_config_text()
    valid, validation_message = validate_yaml_text(content)

    return templates.TemplateResponse(
        request,
        "config_editor.html",
        {
            "request": request,
            "page_title": "Config Editor",
            "content": content,
            "valid": valid,
            "validation_message": validation_message,
            "result": None,
        },
    )


@router.post("/config/save")
def config_save(request: Request, content: str = Form(...)):
    valid, validation_message = validate_yaml_text(content)
    result = save_config(content) if valid else {"ok": False, "message": validation_message}

    return templates.TemplateResponse(
        request,
        "config_editor.html",
        {
            "request": request,
            "page_title": "Config Editor",
            "content": content,
            "valid": valid,
            "validation_message": validation_message,
            "result": result,
        },
    )
