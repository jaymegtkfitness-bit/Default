"""
Central Claude agentic loop.
Receives a user message, builds context, calls Claude, dispatches tool calls,
and returns the final text response.
"""
import json
import structlog
from anthropic import AsyncAnthropic
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core import tools as tool_defs
from app.core import memory
from app.core.prompts import build_system_prompt

log = structlog.get_logger()
_client = AsyncAnthropic(api_key=settings.anthropic_api_key)

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 4096


async def _dispatch_tool(
    name: str,
    tool_input: dict,
    db: AsyncSession,
) -> str:
    """Execute a tool call and return the result as a string."""

    if name == "create_action_item":
        item = await memory.create_action_item(
            db,
            description=tool_input["description"],
            client_name=tool_input.get("client_name"),
            due_date=tool_input.get("due_date"),
            priority=tool_input.get("priority", "normal"),
        )
        return json.dumps({"id": item.id, "description": item.description, "status": "created"})

    if name == "complete_action_item":
        success = await memory.complete_action_item(db, tool_input["action_item_id"])
        return json.dumps({"success": success})

    if name == "list_pending_action_items":
        items = await memory.get_pending_action_items(
            db,
            client_name=tool_input.get("client_name"),
            priority=tool_input.get("priority"),
        )
        return json.dumps([
            {
                "id": i.id,
                "description": i.description,
                "client_name": i.client_name,
                "due_date": i.due_date,
                "priority": i.priority,
                "created_at": i.created_at.isoformat(),
            }
            for i in items
        ])

    if name == "add_client_note":
        note = await memory.add_client_note(db, tool_input["client_name"], tool_input["note"])
        return json.dumps({"id": note.id, "status": "saved"})

    if name == "get_client_notes":
        notes = await memory.get_client_notes(db, tool_input["client_name"])
        return json.dumps([
            {"id": n.id, "note": n.note, "created_at": n.created_at.isoformat()}
            for n in notes
        ])

    if name == "draft_content":
        # The actual drafting happens in Claude's response — this tool signals the intent.
        # Return the parameters so Claude can write the draft in its final turn.
        return json.dumps({
            "status": "ready_to_draft",
            "content_type": tool_input["content_type"],
            "topic": tool_input["topic"],
            "target_audience": tool_input.get("target_audience", "Rachel avatar — women 35–55"),
            "key_points": tool_input.get("key_points", []),
            "call_to_action": tool_input.get("call_to_action", ""),
            "instruction": (
                "Now write the draft using Jayme's voice from the Brand Engine. "
                "Direct. Grounded. Convicting. No banned words. "
                "Present it clearly so Jayme can review and approve before it goes anywhere."
            ),
        })

    log.warning("unknown_tool", name=name)
    return json.dumps({"error": f"Unknown tool: {name}"})


async def run(
    user_message: str,
    session_id: str,
    db: AsyncSession,
) -> str:
    """
    Run the full agentic loop for a user message.
    Returns the final text response to send to Telegram.
    """
    pending_count, high_priority = await memory.get_context_summary(db)
    system_prompt = build_system_prompt(
        pending_action_count=pending_count,
        high_priority_items=high_priority,
    )

    history = await memory.load_history(db, session_id)
    await memory.save_turn(db, session_id, "user", user_message)

    messages = history + [{"role": "user", "content": user_message}]

    final_text = ""
    iteration = 0
    max_iterations = 10  # safety cap

    while iteration < max_iterations:
        iteration += 1
        log.info("agent_call", iteration=iteration, session_id=session_id)

        response = await _client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system_prompt,
            tools=tool_defs.TOOLS,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            # Extract text from response
            for block in response.content:
                if hasattr(block, "text"):
                    final_text = block.text
                    break
            break

        if response.stop_reason == "tool_use":
            # Append assistant message (may contain both text and tool_use blocks)
            assistant_content = []
            for block in response.content:
                if hasattr(block, "text") and block.text:
                    assistant_content.append({"type": "text", "text": block.text})
                elif block.type == "tool_use":
                    assistant_content.append({
                        "type": "tool_use",
                        "id": block.id,
                        "name": block.name,
                        "input": block.input,
                    })
            messages.append({"role": "assistant", "content": assistant_content})

            # Execute all tool calls
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    log.info("tool_call", name=block.name, input=block.input)
                    result = await _dispatch_tool(block.name, block.input, db)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })

            messages.append({"role": "user", "content": tool_results})
            continue

        # Unexpected stop reason
        log.warning("unexpected_stop_reason", reason=response.stop_reason)
        break

    if final_text:
        await memory.save_turn(db, session_id, "assistant", final_text)

    return final_text or "Something went wrong — no response from Claude."
