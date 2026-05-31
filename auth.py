"""
Run once to authenticate with Too Good To Go.
TGTG will email a PIN code to your address; enter it when prompted.
Saves credentials to credentials.json for use by monitor.py.
"""

import json
from tgtg import TgtgClient
from config import EMAIL, CREDENTIALS_FILE


def main():
    print(f"Requesting login PIN for {EMAIL}...")
    client = TgtgClient(email=EMAIL)

    creds = client.get_credentials()
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(creds, f, indent=2)

    print(f"Credentials saved to {CREDENTIALS_FILE}")
    print("Run monitor.py to start watching your favorites.")


if __name__ == "__main__":
    main()
