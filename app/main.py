from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers.actions import router as actions_router
from app.routers.backups import router as backups_router
from app.routers.config_editor import router as config_router
from app.routers.dashboard import router as dashboard_router
from app.routers.devices import router as devices_router
from app.routers.llm import router as llm_router
from app.routers.logs import router as logs_router

app = FastAPI(title="Xiaozhi Admin UI", version="0.1.0")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(dashboard_router)
app.include_router(config_router)
app.include_router(actions_router)
app.include_router(logs_router)
app.include_router(devices_router)
app.include_router(llm_router)
app.include_router(backups_router)

