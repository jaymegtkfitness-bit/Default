"""
Telegram bot — the primary interface for Jayme.
Runs in polling mode for Phase 1.
"""
import structlog
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.constants import ParseMode

from app.config import settings
from app.core import agent
from app.db.session import AsyncSessionLocal
from app.core import memory
from app.telegram.notifications import format_action_list, format_daily_briefing

log = structlog.get_logger()

OWNER_ID = settings.telegram_owner_chat_id


def _is_owner(update: Update) -> bool:
    return update.effective_user and update.effective_user.id == OWNER_ID


async def _send(update: Update, text: str) -> None:
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


# ── Command handlers ────────────────────────────────────────────────────────


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_owner(update):
        return
    await _send(
        update,
        "*Legacy Performance AI Executive Assistant is online.*\n\n"
        "I know your business, your brand, and your clients. "
        "Talk to me like you'd talk to your chief of staff.\n\n"
        "Commands:\n"
        "/actions — list open action items\n"
        "/briefing — get your daily briefing\n"
        "/help — show this message",
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_owner(update):
        return
    await _send(
        update,
        "*Commands*\n"
        "/actions — list all open action items\n"
        "/briefing — morning briefing (items + context)\n"
        "/help — this message\n\n"
        "Or just talk to me naturally:\n"
        "— \"What's Sarah's status?\"\n"
        "— \"Draft a caption about why cardio isn't the answer\"\n"
        "— \"Remind me to send Mike his program by Friday\"\n"
        "— \"Mark action item 3 done\"",
    )


async def cmd_actions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_owner(update):
        return
    async with AsyncSessionLocal() as db:
        items = await memory.get_pending_action_items(db)
    await _send(update, format_action_list(items))


async def cmd_briefing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_owner(update):
        return
    async with AsyncSessionLocal() as db:
        items = await memory.get_pending_action_items(db)
    await _send(update, format_daily_briefing(items))


# ── Message handler ──────────────────────────────────────────────────────────


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_owner(update):
        return

    user_text = update.message.text
    session_id = str(update.effective_chat.id)

    await update.message.chat.send_action("typing")

    try:
        async with AsyncSessionLocal() as db:
            response = await agent.run(user_text, session_id, db)
        await _send(update, response)
    except Exception as exc:
        log.error("agent_error", error=str(exc), exc_info=True)
        await _send(update, f"Something went wrong: {exc}")


# ── App setup ────────────────────────────────────────────────────────────────


def build_app() -> Application:
    app = Application.builder().token(settings.telegram_bot_token).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("actions", cmd_actions))
    app.add_handler(CommandHandler("briefing", cmd_briefing))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    return app


async def set_commands(app: Application) -> None:
    await app.bot.set_my_commands([
        BotCommand("actions", "List open action items"),
        BotCommand("briefing", "Get your daily briefing"),
        BotCommand("help", "Show commands"),
    ])
