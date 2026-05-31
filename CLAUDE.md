# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A polling monitor for Too Good To Go favorites. It watches the user's saved favorites and sends an SMS via textbelt.com when an item goes from sold-out to available.

## Setup & usage

```bash
pip install -r requirements.txt

# Edit config.py with your email, phone number, and textbelt key

# One-time auth (sends magic link email, waits for click)
python auth.py

# Start monitoring
python monitor.py
```

## Architecture

Three files:

- **`config.py`** — all user-configurable values (email, phone, textbelt key, poll interval, credentials file path)
- **`auth.py`** — one-time login flow; creates `credentials.json` with access/refresh tokens and cookie
- **`monitor.py`** — polling loop; loads credentials, calls `TgtgClient.get_items()` (returns favorites by default), texts on 0→available transitions, re-saves credentials after each poll to persist any token refreshes

## Key behaviors

- First poll is silent (establishes baseline state); alerts only fire on transitions after that
- Credentials are re-persisted after every poll to catch auto-refreshed tokens
- Poll interval defaults to 60s — keep it above 15s to avoid TGTG rate limiting
- `get_items()` with no args returns the authenticated user's favorites list
