"""
Zoom Server-to-Server OAuth client.

Setup required:
  1. Go to developers.zoom.us → Build App → Server-to-Server OAuth
  2. Activate the app and copy ACCOUNT_ID, CLIENT_ID, CLIENT_SECRET
  3. Add scopes: recording:read:admin  (or recording:read:list_user_recordings)
  4. Set ZOOM_ACCOUNT_ID, ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET in .env
"""
import base64
import re
from datetime import datetime, timedelta, timezone

import httpx
import structlog

from app.config import settings

log = structlog.get_logger()

_TOKEN_URL = "https://zoom.us/oauth/token"
_API_BASE = "https://api.zoom.us/v2"

_cached_token: str | None = None
_token_expires_at: datetime | None = None


def _is_configured() -> bool:
    return bool(settings.zoom_account_id and settings.zoom_client_id and settings.zoom_client_secret)


async def _get_access_token() -> str:
    global _cached_token, _token_expires_at

    now = datetime.now(timezone.utc)
    if _cached_token and _token_expires_at and now < _token_expires_at:
        return _cached_token

    credentials = base64.b64encode(
        f"{settings.zoom_client_id}:{settings.zoom_client_secret}".encode()
    ).decode()

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            _TOKEN_URL,
            params={"grant_type": "account_credentials", "account_id": settings.zoom_account_id},
            headers={"Authorization": f"Basic {credentials}"},
        )
        resp.raise_for_status()
        data = resp.json()

    _cached_token = data["access_token"]
    expires_in = data.get("expires_in", 3600)
    _token_expires_at = now + timedelta(seconds=expires_in - 60)
    return _cached_token


def _parse_vtt(vtt_bytes: bytes) -> str:
    text = vtt_bytes.decode("utf-8", errors="replace")
    lines = text.splitlines()
    segments: list[str] = []
    current: list[str] = []

    for line in lines:
        line = line.strip()
        if not line or line == "WEBVTT" or re.match(r"^\d+$", line):
            if current:
                segments.append(" ".join(current))
                current = []
            continue
        if re.match(r"^\d{2}:\d{2}:\d{2}", line):
            if current:
                segments.append(" ".join(current))
                current = []
            continue
        cleaned = re.sub(r"<[^>]+>", "", line).strip()
        if cleaned:
            current.append(cleaned)

    if current:
        segments.append(" ".join(current))

    return "\n".join(segments)


async def list_recent_recordings(days: int = 7) -> list[dict]:
    if not _is_configured():
        return []

    token = await _get_access_token()
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{_API_BASE}/users/me/recordings",
            headers={"Authorization": f"Bearer {token}"},
            params={
                "from": start.strftime("%Y-%m-%d"),
                "to": end.strftime("%Y-%m-%d"),
                "page_size": 20,
            },
        )
        resp.raise_for_status()
        data = resp.json()

    meetings = data.get("meetings", [])
    results = []
    for m in meetings:
        transcript_file = next(
            (f for f in m.get("recording_files", []) if f.get("file_type") == "TRANSCRIPT"),
            None,
        )
        if not transcript_file:
            continue
        results.append({
            "meeting_id": m.get("id"),
            "topic": m.get("topic", "Untitled"),
            "start_time": m.get("start_time"),
            "duration_minutes": m.get("duration", 0),
            "transcript_url": transcript_file.get("download_url"),
        })
    return results


async def download_transcript(url: str) -> str:
    token = await _get_access_token()
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(url, headers={"Authorization": f"Bearer {token}"})
        resp.raise_for_status()
        return _parse_vtt(resp.content)


async def get_recent_transcripts(days: int = 7) -> list[dict]:
    if not _is_configured():
        return [{"error": "Zoom credentials not configured. Add ZOOM_ACCOUNT_ID, ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET to .env"}]

    try:
        recordings = await list_recent_recordings(days=days)
        if not recordings:
            return [{"info": f"No recordings with transcripts found in the last {days} days."}]

        results = []
        for rec in recordings[:3]:
            try:
                transcript_text = await download_transcript(rec["transcript_url"])
                results.append({
                    "topic": rec["topic"],
                    "start_time": rec["start_time"],
                    "duration_minutes": rec["duration_minutes"],
                    "transcript": transcript_text[:8000],
                })
            except Exception as e:
                log.error("transcript_download_failed", topic=rec["topic"], error=str(e))
                results.append({"topic": rec["topic"], "error": str(e)})

        return results
    except Exception as e:
        log.error("zoom_get_transcripts_failed", error=str(e))
        return [{"error": str(e)}]
