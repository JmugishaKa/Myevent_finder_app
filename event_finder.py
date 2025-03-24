import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Load API key
load_dotenv()
API_KEY = os.getenv("TICKETMASTER_API_KEY")
BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"

def fetch_events(city, event_type=None):
    """Fetch events from Ticketmaster API."""
    params = {
        "apikey": API_KEY,
        "city": city,
        "size": 10,  # Limit to 10 events
    }
    if event_type:
        params["classificationName"] = event_type

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("_embedded", {}).get("events", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching events: {e}")
        return []

def display_events(events, sort_by="name"):
    """Display events sorted by name or date."""
    if not events:
        print("No events found.")
        return

    # Sort events
    if sort_by == "date":
        events.sort(key=lambda x: x.get("dates", {}).get("start", {}).get("localDate", "9999-12-31") or "9999-12-31")
    else:
        events.sort(key=lambda x: x.get("name", "").lower())

    print("\nEvents:")
    for i, event in enumerate(events, 1):
        name = event.get("name", "Unknown Event")
        date = event.get("dates", {}).get("start", {}).get("localDate", "TBD")
        print(f"{i}. {name} - Date: {date}")

def main():
    """Main CLI loop."""
    print("Welcome to Local Event Finder!")
    while True:
        city = input("\nEnter a city (or 'quit' to exit): ").strip()
        if city.lower() == "quit":
            print("Goodbye!")
            break

        event_type = input("Enter event type (e.g., music, sports) or press Enter to skip: ").strip() or None
        events = fetch_events(city, event_type)

        if events:
            sort_by = input("Sort by (name/date): ").strip().lower() or "name"
            if sort_by not in ["name", "date"]:
                print("Invalid sort option. Using 'name'.")
                sort_by = "name"
            display_events(events, sort_by)
        else:
            print("Try another city or check your connection.")

if __name__ == "__main__":
    main()
