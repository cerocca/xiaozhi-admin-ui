from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.backup_service import (
    list_backups,
    delete_backup,
    delete_all_backups,
)
from app.services.config_service import restore_backup

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/backups")
def backups_page(request: Request):
    backups = list_backups()
    return templates.TemplateResponse(
        request,
        "backups.html",
        {
            "request": request,
            "page_title": "Backups",
            "backups": backups,
            "result": None,
        },
    )


@router.post("/backups/restore")
async def restore_backup_route(request: Request):
    form = await request.form()
    filename = form.get("filename")

    try:
        restore_backup(filename)
        result = {"ok": True, "message": f"Backup ripristinato: {filename}"}
    except Exception as e:
        result = {"ok": False, "message": str(e)}

    backups = list_backups()

    return templates.TemplateResponse(
        request,
        "backups.html",
        {
            "request": request,
            "page_title": "Backups",
            "backups": backups,
            "result": result,
        },
    )


@router.post("/backups/delete")
async def delete_backup_route(request: Request):
    form = await request.form()
    filename = form.get("filename")

    result = delete_backup(filename)
    backups = list_backups()

    return templates.TemplateResponse(
        request,
        "backups.html",
        {
            "request": request,
            "page_title": "Backups",
            "backups": backups,
            "result": result,
        },
    )


@router.post("/backups/delete-all")
async def delete_all_backups_route(request: Request):
    result = delete_all_backups()
    backups = list_backups()

    return templates.TemplateResponse(
        request,
        "backups.html",
        {
            "request": request,
            "page_title": "Backups",
            "backups": backups,
            "result": result,
        },
    )
