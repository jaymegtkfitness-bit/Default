"""
Claude tool definitions for Phase 1.
Phase 2+ will add GHL, Everfit, Skool, Zoom, and knowledge-base tools.
"""

TOOLS = [
    {
        "name": "create_action_item",
        "description": (
            "Create a new action item to track something that needs to be done. "
            "Use this when Jayme mentions a task, follow-up, or commitment — even implicitly. "
            "Always create one when a client conversation surfaces a next step."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": "Clear description of what needs to be done",
                },
                "client_name": {
                    "type": "string",
                    "description": "Client name if this task is related to a specific client",
                },
                "due_date": {
                    "type": "string",
                    "description": "Due date in YYYY-MM-DD format if known or implied",
                },
                "priority": {
                    "type": "string",
                    "enum": ["high", "normal", "low"],
                    "description": "Priority level — default normal",
                },
            },
            "required": ["description"],
        },
    },
    {
        "name": "complete_action_item",
        "description": "Mark an action item as completed.",
        "input_schema": {
            "type": "object",
            "properties": {
                "action_item_id": {
                    "type": "integer",
                    "description": "The numeric ID of the action item to mark complete",
                },
            },
            "required": ["action_item_id"],
        },
    },
    {
        "name": "list_pending_action_items",
        "description": (
            "List all pending (incomplete) action items. "
            "Use this when Jayme asks what's outstanding, or when building a briefing."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "client_name": {
                    "type": "string",
                    "description": "Filter by client name (optional)",
                },
                "priority": {
                    "type": "string",
                    "enum": ["high", "normal", "low"],
                    "description": "Filter by priority (optional)",
                },
            },
            "required": [],
        },
    },
    {
        "name": "add_client_note",
        "description": (
            "Save a note about a client for future reference. "
            "Use this after learning something new about a client — their goals, struggles, "
            "program updates, or anything worth remembering."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "client_name": {
                    "type": "string",
                    "description": "Client's name",
                },
                "note": {
                    "type": "string",
                    "description": "The note to save",
                },
            },
            "required": ["client_name", "note"],
        },
    },
    {
        "name": "get_client_notes",
        "description": "Retrieve saved notes about a specific client.",
        "input_schema": {
            "type": "object",
            "properties": {
                "client_name": {
                    "type": "string",
                    "description": "Client's name",
                },
            },
            "required": ["client_name"],
        },
    },
    {
        "name": "draft_content",
        "description": (
            "Draft a piece of content in Jayme's voice — a social caption, email, DM, "
            "Skool post, or workshop hook. The draft will be shown to Jayme for approval "
            "before any posting or sending occurs. Always call this instead of writing "
            "content inline when the output is something that would be published or sent."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "content_type": {
                    "type": "string",
                    "enum": ["caption", "email", "dm", "skool_post", "hook", "workshop_open"],
                    "description": "What type of content to draft",
                },
                "topic": {
                    "type": "string",
                    "description": "The topic or subject of the content",
                },
                "target_audience": {
                    "type": "string",
                    "description": "Who this is for (e.g., 'Rachel avatar', 'existing Built to Last members')",
                },
                "key_points": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Key points or angles to hit",
                },
                "call_to_action": {
                    "type": "string",
                    "description": "Desired CTA if any (e.g., 'book a call', 'reply to this email')",
                },
            },
            "required": ["content_type", "topic"],
        },
    },
]
