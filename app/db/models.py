from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(64), nullable=False, index=True)
    role = Column(String(16), nullable=False)  # user | assistant | tool_result
    content = Column(Text, nullable=False)
    tool_name = Column(String(64), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class ActionItem(Base):
    __tablename__ = "action_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text, nullable=False)
    client_name = Column(String(128), nullable=True, index=True)
    due_date = Column(String(16), nullable=True)  # YYYY-MM-DD
    priority = Column(String(8), default="normal", nullable=False)  # high | normal | low
    status = Column(String(16), default="pending", nullable=False)  # pending | completed | snoozed
    source = Column(String(32), default="manual", nullable=False)   # manual | zoom_call | scheduled
    source_ref = Column(String(64), nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    reminders = relationship("ScheduledReminder", back_populates="action_item", cascade="all, delete-orphan")


class ClientNote(Base):
    __tablename__ = "client_notes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_name = Column(String(128), nullable=False, index=True)
    note = Column(Text, nullable=False)
    source = Column(String(32), default="agent", nullable=False)  # agent | zoom_call | manual
    source_ref = Column(String(64), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class CallSummary(Base):
    __tablename__ = "call_summaries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    zoom_meeting_id = Column(String(64), nullable=True, unique=True)
    meeting_topic = Column(String(256), nullable=True)
    meeting_date = Column(DateTime, nullable=True)
    participants = Column(Text, nullable=True)  # JSON string
    raw_transcript = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    action_items_extracted = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class ScheduledReminder(Base):
    __tablename__ = "scheduled_reminders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    action_item_id = Column(Integer, ForeignKey("action_items.id"), nullable=False)
    remind_at = Column(DateTime, nullable=False)
    sent = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    action_item = relationship("ActionItem", back_populates="reminders")
