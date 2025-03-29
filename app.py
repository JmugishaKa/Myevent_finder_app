from flask import Flask, request, render_template
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__, static_folder="static", template_folder="templates")
load_dotenv()
TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")
EVENTBRITE_API_KEY = os.getenv("EVENTBRITE_API_KEY")
TM_BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"
EB_BASE_URL = "https://www.eventbriteapi.com/v3/events/search/"

def fetch_events(city, event_type=None):
    events = []
    tm_params = {"apikey": TICKETMASTER_API_KEY, "city": city.title(), "size": 10}
    if event_type:
        tm_params["classificationName"] = event_type
    try:
        response = requests.get(TM_BASE_URL, params=tm_params)
        events.extend(response.json().get("_embedded", {}).get("events", []))
    except Exception as e:
        print(f"Ticketmaster error: {e}")
    eb_headers = {"Authorization": f"Bearer {EVENTBRITE_API_KEY}"}
    eb_params = {"q": city.title()}
    if event_type:
        eb_params["categories"] = event_type
    try:
        response = requests.get(EB_BASE_URL, headers=eb_headers, params=eb_params)
        eb_events = [{"name": e["name"]["text"], "dates": {"start": {"localDate": e["start"]["local"][:10]}}} 
                     for e in response.json().get("events", [])]
        events.extend(eb_events)
    except Exception as e:
        print(f"Eventbrite error: {e}")
    return events

@app.route("/", methods=["GET", "POST"])
def index():
    events = []
    error = None
    if request.method == "POST":
        city = request.form.get("city")
        event_type = request.form.get("event_type") or None
        sort_by = request.form.get("sort_by", "name")
        events = fetch_events(city, event_type)
        if not events:
            error = "No events found."
        elif sort_by == "date":
            events.sort(key=lambda x: x.get("dates", {}).get("start", {}).get("localDate", "9999-12-31"))
        else:
            events.sort(key=lambda x: x.get("name", "").lower())
    return render_template("index.html", events=events, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
