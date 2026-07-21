from datetime import datetime
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from pathlib import Path
from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.db.models import ActionItem, CallSummary
from app.core import memory

router = APIRouter()


def _dashboard_html() -> str:
    path = Path(__file__).parent / "dashboard.html"
    return path.read_text(encoding="utf-8")


@router.get("/", response_class=HTMLResponse)
async def dashboard():
    return _dashboard_html()


@router.get("/api/actions")
async def list_actions(client: str | None = None, priority: str | None = None):
    async with AsyncSessionLocal() as db:
        items = await memory.get_pending_action_items(db, client_name=client, priority=priority)
    return [
        {
            "id": i.id,
            "description": i.description,
            "client_name": i.client_name,
            "due_date": i.due_date,
            "priority": i.priority,
            "source": i.source,
            "created_at": i.created_at.isoformat(),
        }
        for i in items
    ]


class CreateActionRequest(BaseModel):
    description: str
    client_name: str | None = None
    due_date: str | None = None
    priority: str = "normal"


@router.post("/api/actions", status_code=201)
async def create_action(body: CreateActionRequest):
    async with AsyncSessionLocal() as db:
        item = await memory.create_action_item(
            db,
            description=body.description,
            client_name=body.client_name,
            due_date=body.due_date,
            priority=body.priority,
            source="dashboard",
        )
    return {"id": item.id, "description": item.description}


@router.post("/api/actions/{item_id}/done")
async def complete_action(item_id: int):
    async with AsyncSessionLocal() as db:
        success = await memory.complete_action_item(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Action item not found or already complete")
    return {"ok": True}


@router.get("/api/calls")
async def list_calls():
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(CallSummary).order_by(CallSummary.created_at.desc()).limit(10)
        )
        calls = result.scalars().all()
    return [
        {
            "id": c.id,
            "meeting_topic": c.meeting_topic,
            "meeting_date": c.meeting_date.isoformat() if c.meeting_date else None,
            "participants": c.participants,
            "summary": c.summary,
            "created_at": c.created_at.isoformat(),
        }
        for c in calls
    ]
