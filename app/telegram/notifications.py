"""
Formatters for proactive Telegram notifications.
"""
from app.db.models import ActionItem


def format_action_item(item: ActionItem) -> str:
    priority_icon = {"high": "🔴", "normal": "🟡", "low": "⚪"}.get(item.priority, "🟡")
    line = f"{priority_icon} [{item.id}] {item.description}"
    if item.client_name:
        line += f" — {item.client_name}"
    if item.due_date:
        line += f" (due {item.due_date})"
    return line


def format_action_list(items: list[ActionItem]) -> str:
    if not items:
        return "No pending action items."
    lines = ["*Pending Action Items*\n"]
    for item in items:
        lines.append(format_action_item(item))
    return "\n".join(lines)


def format_daily_briefing(
    action_items: list[ActionItem],
    additional_notes: str = "",
) -> str:
    lines = ["*Good morning — here's your day.*\n"]

    high = [i for i in action_items if i.priority == "high"]
    if high:
        lines.append(f"*High priority ({len(high)}):*")
        for item in high:
            lines.append(f"  🔴 [{item.id}] {item.description}" + (f" — {item.client_name}" if item.client_name else ""))
        lines.append("")

    normal = [i for i in action_items if i.priority == "normal"]
    if normal:
        lines.append(f"*Action items ({len(normal)}):*")
        for item in normal[:5]:  # Cap at 5 for readability
            lines.append(f"  🟡 [{item.id}] {item.description}" + (f" — {item.client_name}" if item.client_name else ""))
        if len(normal) > 5:
            lines.append(f"  ... and {len(normal) - 5} more")
        lines.append("")

    if additional_notes:
        lines.append(additional_notes)

    if not high and not normal:
        lines.append("No open action items. Clean slate.")

    return "\n".join(lines)
