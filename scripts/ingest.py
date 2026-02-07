"""Fetch cultural events from OpenAgenda and save them as JSONL."""

import requests
import json
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

OUTPUT_FILE = Path("data/events.jsonl")
API_KEY = os.getenv("OPENAGENDA_API_KEY")

def fetch_events_from_agenda(agenda_uid):
    """Fetch events from a single OpenAgenda agenda UID."""
    print(f"Fetching events from agenda {agenda_uid}...")

    url = f"https://api.openagenda.com/v2/agendas/{agenda_uid}/events"

    all_events = []
    page = 1
    per_page = 100
    total_fetched = 0
    total_events = None

    while True:
        params = {
            "key": API_KEY,
            "page": page,
            "limit": per_page,
            "filters": {
                "date": {
                    "from": "2025-01-01",
                    "to": "2025-12-31"
                }
            },
            "detailed": 1
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        json_response = response.json()

        if total_events is None:
            total_events = json_response.get("total", 0)

        events = json_response.get("events", [])
        if not events:
            break

        print(f"Fetched page {page} with {len(events)} events.")
        all_events.extend(events)
        total_fetched += len(events)
        page += 1

        if total_fetched >= total_events:
            break

    return all_events


def fetch_all_agendas(max_agendas=None):
    """Fetch events from all agendas (optionally capped)."""
    print("Fetching all agendas from OpenAgenda...")
    agenda_url = f"https://api.openagenda.com/v2/agendas?key={API_KEY}"
    response = requests.get(agenda_url)
    response.raise_for_status()
    data = response.json()

    all_events = []
    for i, agenda in enumerate(data.get("agendas", [])):
        if max_agendas is not None and i >= max_agendas:
            break
        uid = agenda.get("uid")
        title = agenda.get("title")
        print(f"Getting agenda {title}")
        if uid:
            events = fetch_events_from_agenda(uid)
            all_events.extend(events)

    print(f"Total {len(all_events)} events fetched from all agendas.")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        for record in all_events:
            json.dump(record, f, ensure_ascii=False)
            f.write("\n")

    print(f"Events saved to {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    fetch_all_agendas(max_agendas=5)
