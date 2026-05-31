import json
import time
import requests
from tgtg import TgtgClient
from config import PHONE_NUMBER, TEXTBELT_KEY, POLL_INTERVAL, CREDENTIALS_FILE


def send_text(message):
    r = requests.post("http://textbelt.com/text", data={
        "key": TEXTBELT_KEY,
        "number": PHONE_NUMBER,
        "message": message,
    })
    result = r.json()
    if not result.get("success"):
        print(f"  [text failed: {result}]")


def load_credentials():
    with open(CREDENTIALS_FILE) as f:
        return json.load(f)


def save_credentials(client):
    creds = client.get_credentials()
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(creds, f, indent=2)


def main():
    creds = load_credentials()
    client = TgtgClient(
        access_token=creds["access_token"],
        refresh_token=creds["refresh_token"],
        cookie=creds["cookie"],
        user_id=creds["user_id"],
    )

    last_state = {}
    first_poll = True

    print("Monitoring favorites... (Ctrl+C to stop)")

    while True:
        try:
            items = client.get_items()

            for item in items:
                item_id = item["item"]["item_id"]
                name = item["display_name"]
                available = item["items_available"]

                if not first_poll:
                    was = last_state.get(item_id, 0)
                    if available > 0 and was == 0:
                        msg = f"TGTG: {name} — {available} available!"
                        print(msg)
                        send_text(msg)
                    elif available == 0 and was > 0:
                        print(f"  {name}: sold out")

                last_state[item_id] = available

            if first_poll:
                avail = sum(1 for i in items if i["items_available"] > 0)
                print(f"Tracking {len(items)} favorites. {avail} currently available.")
                first_poll = False

            save_credentials(client)

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
