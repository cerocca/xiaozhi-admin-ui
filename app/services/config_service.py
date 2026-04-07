from __future__ import annotations

import hashlib
import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path

import yaml

from app.config import settings


BACKUP_DIR = Path("/home/ciru/xiaozhi-admin-ui/data/backups/config")


def get_config_path() -> Path:
    return Path(settings.xiaozhi_config)


def ensure_backup_dir() -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    return BACKUP_DIR


def read_config_text() -> str:
    path = get_config_path()
    return path.read_text(encoding="utf-8")


def validate_yaml_text(content: str) -> tuple[bool, str]:
    try:
        yaml.safe_load(content)
        return True, "YAML valido"
    except yaml.YAMLError as e:
        return False, str(e)


def compute_sha256(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def create_backup() -> Path:
    src = get_config_path()
    if not src.exists():
        raise FileNotFoundError(f"Config non trovata: {src}")

    ensure_backup_dir()
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    dst = BACKUP_DIR / f"{timestamp}.config.yaml"
    shutil.copy2(src, dst)
    return dst


def atomic_write_config(content: str) -> None:
    target = get_config_path()
    target.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=str(target.parent),
        delete=False,
    ) as tmp:
        tmp.write(content)
        tmp.flush()
        os.fsync(tmp.fileno())
        temp_name = tmp.name

    os.replace(temp_name, target)


def save_config(content: str) -> dict:
    valid, message = validate_yaml_text(content)
    if not valid:
        return {
            "ok": False,
            "message": f"Validazione YAML fallita: {message}",
        }

    backup_path = create_backup()
    atomic_write_config(content)

    return {
        "ok": True,
        "message": "Config salvata correttamente",
        "backup_path": str(backup_path),
        "sha256": compute_sha256(content),
    }


def list_backups() -> list[dict]:
    ensure_backup_dir()
    backups = []

    for path in sorted(BACKUP_DIR.glob("*.config.yaml"), reverse=True):
        text = path.read_text(encoding="utf-8")
        stat = path.stat()
        backups.append(
            {
                "name": path.name,
                "path": str(path),
                "size": stat.st_size,
                "mtime": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "sha256_short": compute_sha256(text)[:12],
            }
        )

    return backups


def restore_backup(filename: str) -> dict:
    ensure_backup_dir()
    backup_file = BACKUP_DIR / filename

    if not backup_file.exists():
        return {"ok": False, "message": f"Backup non trovato: {filename}"}

    content = backup_file.read_text(encoding="utf-8")
    valid, message = validate_yaml_text(content)
    if not valid:
        return {
            "ok": False,
            "message": f"Il backup non contiene YAML valido: {message}",
        }

    current_backup = create_backup()
    atomic_write_config(content)

    return {
        "ok": True,
        "message": "Rollback completato",
        "restored_from": filename,
        "pre_restore_backup": str(current_backup),
    }
