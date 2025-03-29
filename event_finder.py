import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TICKETMASTER_API_KEY")
BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"

def fetch_events(city, event_type=None):
    city = city.title()
    params = {"apikey": API_KEY, "city": city, "size": 10}
    if event_type:
        params["classificationName"] = event_type
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json().get("_embedded", {}).get("events", [])
    except requests.exceptions.RequestException:
        return []

while True:
    city = input("Enter city (or 'quit'): ").strip()
    if city.lower() == "quit":
        break
    event_type = input("Event type (optional): ").strip() or None
    sort_by = input("Sort by (name/date): ").strip()
    events = fetch_events(city, event_type)
    if not events:
        print("No events found.")
    else:
        if sort_by == "date":
            events.sort(key=lambda x: x.get("dates", {}).get("start", {}).get("localDate", "9999-12-31"))
        else:
            events.sort(key=lambda x: x.get("name", "").lower())
        print("\nEvents:")
        for i, event in enumerate(events, 1):
            date = event.get("dates", {}).get("start", {}).get("localDate", "TBD")
            print(f"{i}. {event['name']} - {date}")
