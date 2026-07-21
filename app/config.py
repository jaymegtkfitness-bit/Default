import json
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

    # Server
    port: int = 8000
    webhook_base_url: str = ""
    secret_key: str = ""

    # GHL
    ghl_client_id: str = ""
    ghl_client_secret: str = ""
    ghl_location_id: str = ""

    # Zoom (Server-to-Server OAuth)
    zoom_account_id: str = ""
    zoom_client_id: str = ""
    zoom_client_secret: str = ""
    zoom_webhook_secret_token: str = ""

    # Google (Service Account)
    google_service_account_json: str = ""   # JSON string or path to .json file
    google_sheets_tasks_id: str = ""         # spreadsheet ID (not the published CSV ID)
    google_sheets_tasks_tab: str = "Tasks"   # tab name within the spreadsheet
    google_drive_transcript_folder_id: str = ""
    google_drive_knowledge_folder_ids: str = ""

    # Everfit
    everfit_api_token: str = ""

    # Skool
    skool_api_key: str = ""
    skool_community_id: str = ""

    @property
    def brand_engine_path(self) -> Path:
        return Path(__file__).parent.parent / "knowledge" / "brand_engine.md"

    @property
    def google_service_account_info(self) -> dict | None:
        val = self.google_service_account_json.strip()
        if not val:
            return None
        if val.startswith("{"):
            return json.loads(val)
        p = Path(val)
        if p.exists():
            return json.loads(p.read_text())
        return None


settings = Settings()
