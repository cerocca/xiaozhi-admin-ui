import os

BACKUP_DIR = "/home/ciru/xiaozhi-admin-ui/data/backups/config"


def list_backups():
    if not os.path.exists(BACKUP_DIR):
        return []

    files = sorted(os.listdir(BACKUP_DIR), reverse=True)
    return files


def delete_backup(filename: str) -> dict:
    try:
        path = os.path.join(BACKUP_DIR, filename)

        if not os.path.isfile(path):
            return {"ok": False, "message": "File non trovato"}

        os.remove(path)
        return {"ok": True, "message": f"Backup eliminato: {filename}"}

    except Exception as e:
        return {"ok": False, "message": str(e)}


def delete_all_backups() -> dict:
    try:
        if not os.path.exists(BACKUP_DIR):
            return {"ok": True, "message": "Nessun backup presente"}

        count = 0
        for f in os.listdir(BACKUP_DIR):
            path = os.path.join(BACKUP_DIR, f)
            if os.path.isfile(path):
                os.remove(path)
                count += 1

        return {"ok": True, "message": f"{count} backup eliminati"}

    except Exception as e:
        return {"ok": False, "message": str(e)}
