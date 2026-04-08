from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.services.tts_service import get_tts_page_data

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/tts")
def tts_page(request: Request):
    return templates.TemplateResponse(
        request,
        "tts.html",
        {
            "request": request,
            "page_title": "TTS",
            **get_tts_page_data(),
        },
    )
