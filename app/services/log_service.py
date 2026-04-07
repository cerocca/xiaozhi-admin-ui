from app.services.command_service import run_command


def get_xserver_logs(lines: int = 200) -> dict:
    return run_command(
        [
            "/home/ciru/xiaozhi-admin-ui/scripts/xserver.sh",
            "logs-web",
            str(lines),
        ],
        timeout=20,
    )


def get_piper_logs(lines: int = 200) -> dict:
    return run_command(
        [
            "/home/ciru/xiaozhi-admin-ui/scripts/piper.sh",
            "logs-web",
            str(lines),
        ],
        timeout=20,
    )
