from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    admin_ui_version: str = "0.2.0"
    admin_ui_repo_url: str = "https://github.com/cerocca/xiaozhi-admin-ui"

    admin_ui_host: str = "192.168.1.69"
    admin_ui_port: int = 8088

    xiaozhi_dir: str = "/home/ciru/xiaozhi-esp32-lightserver"
    xiaozhi_config: str = "/home/ciru/xiaozhi-esp32-lightserver/data/.config.yaml"

    piper_health_url: str = "http://127.0.0.1:8091/health"
    piper_systemd_service: str = "piper-api"

    lan_cidr: str = "192.168.1.0/24"


settings = Settings()
