from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Core
    anthropic_api_key: str
    telegram_bot_token: str
    telegram_owner_chat_id: int

    # Database
    database_url: str = "sqlite+aiosqlite:///./legacy_performance.db"

    # Phase 2+
    webhook_base_url: str = ""
    secret_key: str = ""

    # GHL
    ghl_client_id: str = ""
    ghl_client_secret: str = ""
    ghl_location_id: str = ""

    # Zoom
    zoom_client_id: str = ""
    zoom_client_secret: str = ""
    zoom_webhook_secret_token: str = ""

    # Google
    google_client_id: str = ""
    google_client_secret: str = ""
    google_drive_folder_ids: str = ""

    # Everfit
    everfit_api_token: str = ""

    # Skool
    skool_api_key: str = ""
    skool_community_id: str = ""

    @property
    def brand_engine_path(self) -> Path:
        return Path(__file__).parent.parent / "knowledge" / "brand_engine.md"


settings = Settings()
