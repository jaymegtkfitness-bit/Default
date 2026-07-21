"""
One-time Gmail authorization script.

Run this ONCE on any machine that has a web browser:
  python scripts/setup_gmail.py

Steps:
  1. Go to console.cloud.google.com → your project
  2. APIs & Services → Library → search "Gmail API" → Enable
  3. APIs & Services → Credentials → Create Credentials → OAuth 2.0 Client ID
     → Application type: Desktop app → Create → Download JSON
  4. Paste the path to that JSON file when prompted below
  5. A browser window opens — sign in with your Gmail account and allow access
  6. Copy the GMAIL_REFRESH_TOKEN value shown and add it to your .env file
"""
import json
import os
import sys
from pathlib import Path


def main():
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        print("Installing required packages...")
        os.system(f"{sys.executable} -m pip install google-auth-oauthlib -q")
        from google_auth_oauthlib.flow import InstalledAppFlow

    SCOPES = [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.modify",
    ]

    print("\n=== Gmail Authorization Setup ===\n")
    print("You need the OAuth 2.0 Client JSON file from Google Cloud Console.")
    print("(APIs & Services → Credentials → Download the Desktop app client JSON)\n")

    client_json_path = input("Path to your OAuth client JSON file: ").strip().strip('"')
    if not Path(client_json_path).exists():
        print(f"File not found: {client_json_path}")
        sys.exit(1)

    flow = InstalledAppFlow.from_client_secrets_file(client_json_path, SCOPES)

    print("\nOpening browser for authorization...")
    print("If the browser doesn't open, copy and visit the URL that appears.\n")

    try:
        creds = flow.run_local_server(port=0)
    except Exception:
        # Fallback for environments without a browser
        creds = flow.run_console()

    refresh_token = creds.refresh_token
    client_id = creds.client_id
    client_secret = creds.client_secret

    print("\n✓ Authorization successful!\n")
    print("Add these lines to your .env file:\n")
    print(f"GMAIL_CLIENT_ID={client_id}")
    print(f"GMAIL_CLIENT_SECRET={client_secret}")
    print(f"GMAIL_REFRESH_TOKEN={refresh_token}")
    print()

    # Offer to append to .env automatically
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        answer = input(f"Automatically append to {env_path}? [y/N]: ").strip().lower()
        if answer == "y":
            with open(env_path, "a") as f:
                f.write(f"\n# Gmail (OAuth2)\n")
                f.write(f"GMAIL_CLIENT_ID={client_id}\n")
                f.write(f"GMAIL_CLIENT_SECRET={client_secret}\n")
                f.write(f"GMAIL_REFRESH_TOKEN={refresh_token}\n")
            print(f"✓ Written to {env_path}")

    print("\nRestart the bot and Gmail access will be active.")


if __name__ == "__main__":
    main()
