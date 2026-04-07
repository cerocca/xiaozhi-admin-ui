from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.services.status_service import get_dashboard_status

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


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
