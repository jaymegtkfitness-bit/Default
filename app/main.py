"""
Entry point — runs the Telegram bot and FastAPI dashboard together.
Run with: python -m app.main
Dashboard available at http://localhost:8000
"""
import asyncio
import threading
import nest_asyncio
import structlog
import uvicorn

from app.config import settings
from app.db.session import init_db
from app.telegram.bot import build_app, set_commands
from app.api.app import fastapi_app

nest_asyncio.apply()
log = structlog.get_logger()


def _start_fastapi() -> None:
    """Run FastAPI in a background daemon thread so it doesn't block the Telegram bot."""
    uvicorn.run(
        fastapi_app,
        host="0.0.0.0",
        port=settings.port,
        log_level="warning",
    )


def main() -> None:
    asyncio.get_event_loop().run_until_complete(init_db())
    log.info("startup", message="Database ready.")

    # Start dashboard in background thread
    thread = threading.Thread(target=_start_fastapi, daemon=True)
    thread.start()
    log.info("startup", message=f"Dashboard running at http://0.0.0.0:{settings.port}")

    app = build_app()
    asyncio.get_event_loop().run_until_complete(set_commands(app))

    log.info("startup", message="Legacy Performance AI Executive Assistant is running.")
    log.info("startup", message="Send a message to your Telegram bot to get started.")

    # Telegram bot runs on the main thread exactly as before
    app.run_polling(drop_pending_updates=True, close_loop=False)


if __name__ == "__main__":
    main()
