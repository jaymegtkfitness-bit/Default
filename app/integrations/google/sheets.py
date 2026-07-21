"""
Google Sheets integration — writes action items to the LP Command Center spreadsheet.

Setup required:
  1. Create a Google Service Account at console.cloud.google.com
  2. Enable the Google Sheets API
  3. Share your spreadsheet with the service account email
  4. Set GOOGLE_SERVICE_ACCOUNT_JSON in .env (paste the full JSON or provide a file path)
  5. Set GOOGLE_SHEETS_TASKS_ID to your spreadsheet ID
  6. Create a tab named "Tasks" in your spreadsheet with these headers in row 1:
     ID | Description | Client | Due Date | Priority | Status | Source | Created At
"""
import asyncio
import structlog
from app.config import settings

log = structlog.get_logger()

_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
_HEADERS = ["ID", "Description", "Client", "Due Date", "Priority", "Status", "Source", "Created At"]


def _is_configured() -> bool:
    return bool(settings.google_service_account_info and settings.google_sheets_tasks_id)


def _sync_ensure_headers(service) -> None:
    tab = settings.google_sheets_tasks_tab
    sid = settings.google_sheets_tasks_id
    result = service.spreadsheets().values().get(
        spreadsheetId=sid,
        range=f"{tab}!A1:H1",
    ).execute()
    if not result.get("values"):
        service.spreadsheets().values().update(
            spreadsheetId=sid,
            range=f"{tab}!A1",
            valueInputOption="USER_ENTERED",
            body={"values": [_HEADERS]},
        ).execute()


def _sync_append(item_id: int, description: str, client_name: str | None,
                 due_date: str | None, priority: str, source: str, created_at: str) -> bool:
    creds_info = settings.google_service_account_info
    if not creds_info:
        return False

    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build

    creds = Credentials.from_service_account_info(creds_info, scopes=_SCOPES)
    service = build("sheets", "v4", credentials=creds)

    _sync_ensure_headers(service)

    row = [item_id, description, client_name or "", due_date or "", priority, "pending", source, created_at]
    service.spreadsheets().values().append(
        spreadsheetId=settings.google_sheets_tasks_id,
        range=f"{settings.google_sheets_tasks_tab}!A:H",
        valueInputOption="USER_ENTERED",
        body={"values": [row]},
    ).execute()
    return True


def _sync_mark_done(item_id: int) -> bool:
    creds_info = settings.google_service_account_info
    if not creds_info:
        return False

    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build

    creds = Credentials.from_service_account_info(creds_info, scopes=_SCOPES)
    service = build("sheets", "v4", credentials=creds)

    sid = settings.google_sheets_tasks_id
    tab = settings.google_sheets_tasks_tab

    result = service.spreadsheets().values().get(
        spreadsheetId=sid,
        range=f"{tab}!A:F",
    ).execute()

    rows = result.get("values", [])
    for idx, row in enumerate(rows):
        if row and str(row[0]) == str(item_id):
            row_number = idx + 1
            service.spreadsheets().values().update(
                spreadsheetId=sid,
                range=f"{tab}!F{row_number}",
                valueInputOption="USER_ENTERED",
                body={"values": [["done"]]},
            ).execute()
            return True
    return False


async def append_action_item(
    item_id: int,
    description: str,
    client_name: str | None,
    due_date: str | None,
    priority: str,
    source: str,
    created_at: str,
) -> bool:
    if not _is_configured():
        return False
    try:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, _sync_append, item_id, description, client_name, due_date, priority, source, created_at
        )
    except Exception as exc:
        log.error("sheets_append_failed", error=str(exc))
        return False


async def mark_done(item_id: int) -> bool:
    if not _is_configured():
        return False
    try:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _sync_mark_done, item_id)
    except Exception as exc:
        log.error("sheets_mark_done_failed", error=str(exc))
        return False
