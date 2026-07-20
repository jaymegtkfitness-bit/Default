"""
Entry point — starts the Telegram bot in polling mode.
Run with: python -m app.main
"""
import asyncio
import structlog
from app.db.session import init_db
from app.telegram.bot import build_app, set_commands

log = structlog.get_logger()


async def main() -> None:
    log.info("startup", message="Initializing database...")
    await init_db()
    log.info("startup", message="Database ready.")

    app = build_app()
    await set_commands(app)

    log.info("startup", message="Legacy Performance AI Executive Assistant is running.")
    log.info("startup", message="Send a message to your Telegram bot to get started.")

    await app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
