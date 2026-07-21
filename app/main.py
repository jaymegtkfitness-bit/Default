"""
Entry point — runs the Telegram bot and FastAPI dashboard together.
Run with: python -m app.main
Dashboard available at http://localhost:8000
"""
import asyncio
import nest_asyncio
import structlog
import uvicorn

from app.config import settings
from app.db.session import init_db
from app.telegram.bot import build_app, set_commands
from app.api.app import fastapi_app

nest_asyncio.apply()
log = structlog.get_logger()


async def _run_all() -> None:
    log.info("startup", message="Initializing database...")
    await init_db()
    log.info("startup", message="Database ready.")

    telegram_app = build_app()
    await set_commands(telegram_app)

    uvicorn_config = uvicorn.Config(
        fastapi_app,
        host="0.0.0.0",
        port=settings.port,
        loop="none",
        log_level="warning",
    )
    server = uvicorn.Server(uvicorn_config)

    await telegram_app.initialize()
    await telegram_app.start()
    await telegram_app.updater.start_polling(drop_pending_updates=True)

    log.info("startup", message=f"Dashboard running at http://0.0.0.0:{settings.port}")
    log.info("startup", message="Legacy Performance AI Executive Assistant is running.")
    log.info("startup", message="Send a message to your Telegram bot to get started.")

    try:
        await server.serve()
    finally:
        await telegram_app.updater.stop()
        await telegram_app.stop()
        await telegram_app.shutdown()


def main() -> None:
    asyncio.get_event_loop().run_until_complete(_run_all())


if __name__ == "__main__":
    main()
