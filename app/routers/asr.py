from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.services.asr_service import get_asr_page_data

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/asr")
def asr_page(request: Request):
    return templates.TemplateResponse(
        request,
        "asr.html",
        {
            "request": request,
            "page_title": "ASR",
            **get_asr_page_data(),
        },
    )
