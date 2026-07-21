"""
Claude tool definitions.
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
    {
        "name": "read_recent_emails",
        "description": (
            "Read recent emails from Jayme's Gmail inbox. Use when Jayme asks to check email, "
            "'any emails from clients?', 'what's in my inbox?', or similar. "
            "After reading, extract any action items and create them with create_action_item. "
            "Flag anything urgent or from clients."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "max_results": {
                    "type": "integer",
                    "description": "How many emails to fetch (default 10, max 20)",
                },
                "unread_only": {
                    "type": "boolean",
                    "description": "Only fetch unread emails (default true)",
                },
            },
            "required": [],
        },
    },
    {
        "name": "search_emails",
        "description": (
            "Search Gmail for specific emails. Use when Jayme asks about emails from a specific "
            "person, on a specific topic, or with a specific keyword. "
            "Supports Gmail search syntax: 'from:name@example.com', 'subject:invoice', etc."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Gmail search query (e.g. 'from:sarah subject:contract', 'is:unread label:important')",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Max emails to return (default 5)",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_recent_zoom_transcripts",
        "description": (
            "Fetch recent Zoom call transcripts. Use when Jayme says 'analyze my last call', "
            "'what did we discuss in my last zoom', or any variation. Returns transcript text "
            "for up to 3 recent recordings. After calling this, summarize the call, identify "
            "the client, extract all action items, and create them with create_action_item."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "days_back": {
                    "type": "integer",
                    "description": "How many days back to look for recordings (default 7, max 30)",
                },
            },
            "required": [],
        },
    },
]
