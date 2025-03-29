import requests
import os
from dotenv import load_dotenv

load_dotenv()
TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")
EVENTBRITE_API_KEY = os.getenv("EVENTBRITE_API_KEY")
TM_BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"
EB_BASE_URL = "https://www.eventbriteapi.com/v3/events/search/"

def fetch_events(city, event_type=None):
<<<<<<< HEAD
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
=======
    events = []
    # Ticketmaster
    tm_params = {"apikey": TICKETMASTER_API_KEY, "city": city.title(), "size": 10}
    if event_type:
        tm_params["classificationName"] = event_type
    try:
        response = requests.get(TM_BASE_URL, params=tm_params)
        events.extend(response.json().get("_embedded", {}).get("events", []))
    except Exception as e:
        print(f"Ticketmaster error: {e}")
    # Eventbrite
    eb_headers = {"Authorization": f"Bearer {EVENTBRITE_API_KEY}"}
    eb_params = {"q": city.title()}
    if event_type:
        eb_params["categories"] = event_type
    try:
        response = requests.get(EB_BASE_URL, headers=eb_headers, params=eb_params)
        eb_events = [{"name": e["name"]["text"], "dates": {"start": {"localDate": e["start"]["local"][:10]}}} for e in response.json().get("events", [])]
        events.extend(eb_events)
    except Exception as e:
        print(f"Eventbrite error: {e}")
    return events
>>>>>>> bbb80adbfc8ec8e2cf85c5acd8eb4f3f6a1bfc47

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
