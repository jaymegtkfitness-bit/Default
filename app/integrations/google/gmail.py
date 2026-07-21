"""
Gmail integration — reads inbox and email threads via OAuth2.

One-time setup:
  1. console.cloud.google.com → your project → APIs & Services → Enable Gmail API
  2. APIs & Services → Credentials → Create Credentials → OAuth 2.0 Client ID → Desktop app
  3. Download the client JSON, then run: python scripts/setup_gmail.py
  4. Paste the code it gives you — saves GMAIL_REFRESH_TOKEN to .env
"""
import asyncio
from datetime import datetime, timezone
from email import message_from_bytes
from email.header import decode_header
import base64
import structlog

from app.config import settings

log = structlog.get_logger()

_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",   # needed to mark as read
]


def _is_configured() -> bool:
    return bool(
        settings.gmail_client_id
        and settings.gmail_client_secret
        and settings.gmail_refresh_token
    )


def _build_service():
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    creds = Credentials(
        token=None,
        refresh_token=settings.gmail_refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.gmail_client_id,
        client_secret=settings.gmail_client_secret,
        scopes=_SCOPES,
    )
    return build("gmail", "v1", credentials=creds)


def _decode_header_value(raw: str) -> str:
    parts = decode_header(raw or "")
    decoded = []
    for chunk, enc in parts:
        if isinstance(chunk, bytes):
            decoded.append(chunk.decode(enc or "utf-8", errors="replace"))
        else:
            decoded.append(chunk)
    return "".join(decoded)


def _extract_body(payload: dict) -> str:
    """Recursively extract plain text body from a Gmail message payload."""
    mime_type = payload.get("mimeType", "")
    body = payload.get("body", {})

    if mime_type == "text/plain":
        data = body.get("data", "")
        if data:
            return base64.urlsafe_b64decode(data + "==").decode("utf-8", errors="replace")
        return ""

    if mime_type.startswith("multipart/"):
        for part in payload.get("parts", []):
            text = _extract_body(part)
            if text:
                return text

    return ""


def _sync_list_emails(query: str = "is:unread in:inbox", max_results: int = 10) -> list[dict]:
    service = _build_service()
    result = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=max_results,
    ).execute()

    messages = result.get("messages", [])
    if not messages:
        return []

    emails = []
    for msg in messages:
        full = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full",
        ).execute()

        headers = {h["name"].lower(): h["value"] for h in full.get("payload", {}).get("headers", [])}
        body = _extract_body(full.get("payload", {}))

        date_raw = headers.get("date", "")
        emails.append({
            "id": full["id"],
            "thread_id": full.get("threadId"),
            "from": _decode_header_value(headers.get("from", "")),
            "to": _decode_header_value(headers.get("to", "")),
            "subject": _decode_header_value(headers.get("subject", "(no subject)")),
            "date": date_raw,
            "snippet": full.get("snippet", ""),
            "body": body[:3000].strip() if body else "",
            "labels": full.get("labelIds", []),
        })

    return emails


def _sync_search_emails(query: str, max_results: int = 5) -> list[dict]:
    return _sync_list_emails(query=query, max_results=max_results)


async def get_recent_emails(max_results: int = 10, unread_only: bool = True) -> list[dict]:
    if not _is_configured():
        return [{"error": "Gmail not configured. Run: python scripts/setup_gmail.py"}]
    try:
        query = "in:inbox" + (" is:unread" if unread_only else "")
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _sync_list_emails, query, max_results)
    except Exception as exc:
        log.error("gmail_fetch_failed", error=str(exc))
        return [{"error": str(exc)}]


async def search_emails(query: str, max_results: int = 5) -> list[dict]:
    if not _is_configured():
        return [{"error": "Gmail not configured. Run: python scripts/setup_gmail.py"}]
    try:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _sync_search_emails, query, max_results)
    except Exception as exc:
        log.error("gmail_search_failed", error=str(exc))
        return [{"error": str(exc)}]
