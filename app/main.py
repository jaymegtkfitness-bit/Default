"""
Entry point — starts the Telegram bot in polling mode.
Run with: python -m app.main
"""
import asyncio
import nest_asyncio
import structlog
from app.db.session import init_db
from app.telegram.bot import build_app, set_commands

nest_asyncio.apply()
log = structlog.get_logger()


async def _startup() -> None:
    log.info("startup", message="Initializing database...")
    await init_db()
    log.info("startup", message="Database ready.")


def main() -> None:
    asyncio.get_event_loop().run_until_complete(_startup())

    app = build_app()
    asyncio.get_event_loop().run_until_complete(set_commands(app))

    log.info("startup", message="Legacy Performance AI Executive Assistant is running.")
    log.info("startup", message="Send a message to your Telegram bot to get started.")

    app.run_polling(drop_pending_updates=True, close_loop=False)


if __name__ == "__main__":
    main()
