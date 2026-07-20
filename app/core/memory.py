"""
Manages conversation history and action item context for the agent.
"""
from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Conversation, ActionItem, ClientNote


MAX_HISTORY_TURNS = 40  # Keep last 40 messages in context


async def load_history(session: AsyncSession, session_id: str) -> list[dict]:
    """Load conversation history for a Telegram chat session."""
    result = await session.execute(
        select(Conversation)
        .where(Conversation.session_id == session_id)
        .order_by(Conversation.created_at.desc())
        .limit(MAX_HISTORY_TURNS)
    )
    rows = list(reversed(result.scalars().all()))

    messages = []
    for row in rows:
        if row.role == "tool_result":
            # Reconstruct tool result format
            messages.append({
                "role": "user",
                "content": [{"type": "tool_result", "tool_use_id": row.tool_name, "content": row.content}],
            })
        else:
            messages.append({"role": row.role, "content": row.content})
    return messages


async def save_turn(
    session: AsyncSession,
    session_id: str,
    role: str,
    content: str,
    tool_name: str | None = None,
) -> None:
    """Persist a conversation turn."""
    row = Conversation(
        session_id=session_id,
        role=role,
        content=content,
        tool_name=tool_name,
    )
    session.add(row)
    await session.commit()


async def get_pending_action_items(
    session: AsyncSession,
    client_name: str | None = None,
    priority: str | None = None,
) -> list[ActionItem]:
    q = select(ActionItem).where(ActionItem.status == "pending")
    if client_name:
        q = q.where(ActionItem.client_name.ilike(f"%{client_name}%"))
    if priority:
        q = q.where(ActionItem.priority == priority)
    q = q.order_by(ActionItem.priority.desc(), ActionItem.created_at.asc())
    result = await session.execute(q)
    return list(result.scalars().all())


async def create_action_item(
    session: AsyncSession,
    description: str,
    client_name: str | None = None,
    due_date: str | None = None,
    priority: str = "normal",
    source: str = "manual",
    source_ref: str | None = None,
) -> ActionItem:
    item = ActionItem(
        description=description,
        client_name=client_name,
        due_date=due_date,
        priority=priority,
        source=source,
        source_ref=source_ref,
    )
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def complete_action_item(session: AsyncSession, action_item_id: int) -> bool:
    result = await session.execute(
        select(ActionItem).where(ActionItem.id == action_item_id, ActionItem.status == "pending")
    )
    item = result.scalar_one_or_none()
    if not item:
        return False
    item.status = "completed"
    item.completed_at = datetime.utcnow()
    await session.commit()
    return True


async def add_client_note(
    session: AsyncSession,
    client_name: str,
    note: str,
    source: str = "agent",
    source_ref: str | None = None,
) -> ClientNote:
    row = ClientNote(client_name=client_name, note=note, source=source, source_ref=source_ref)
    session.add(row)
    await session.commit()
    await session.refresh(row)
    return row


async def get_client_notes(session: AsyncSession, client_name: str) -> list[ClientNote]:
    result = await session.execute(
        select(ClientNote)
        .where(ClientNote.client_name.ilike(f"%{client_name}%"))
        .order_by(ClientNote.created_at.desc())
        .limit(20)
    )
    return list(result.scalars().all())


async def get_context_summary(session: AsyncSession) -> tuple[int, list[str]]:
    """Return (pending_count, high_priority_descriptions) for system prompt injection."""
    all_pending = await get_pending_action_items(session)
    high_priority = [i for i in all_pending if i.priority == "high"]
    descriptions = [
        f"{i.description}" + (f" ({i.client_name})" if i.client_name else "")
        for i in high_priority[:5]
    ]
    return len(all_pending), descriptions
