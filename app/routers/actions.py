from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.services.command_service import run_command

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.post("/actions/xserver/restart")
def restart_xserver(request: Request):
    result = run_command(
        ["/home/ciru/xiaozhi-admin-ui/scripts/xserver.sh", "restart"],
        timeout=30,
    )
    return templates.TemplateResponse(
        request,
        "action_result.html",
        {
            "request": request,
            "title": "Restart Xiaozhi server",
            "result": result,
        },
    )


@router.post("/actions/piper/restart")
def restart_piper(request: Request):
    result = run_command(
        ["/home/ciru/xiaozhi-admin-ui/scripts/piper.sh", "restart"],
        timeout=30,
    )
    return templates.TemplateResponse(
        request,
        "action_result.html",
        {
            "request": request,
            "title": "Restart Piper",
            "result": result,
        },
    )
