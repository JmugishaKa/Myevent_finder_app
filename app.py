from flask import Flask, request, render_template_string
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
API_KEY = os.getenv("TICKETMASTER_API_KEY")
BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"

def fetch_events(city, event_type=None):
    params = {"apikey": API_KEY, "city": city, "size": 10}
    if event_type:
        params["classificationName"] = event_type
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json().get("_embedded", {}).get("events", [])
    except requests.exceptions.RequestException:
        return []

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

    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head><title>Local Event Finder</title>
        <style>body { font-family: Arial, sans-serif; padding: 20px; }</style>
        </head>
        <body>
            <h1>Local Event Finder</h1>
            <form method="post">
                <input type="text" name="city" placeholder="Enter city" required>
                <input type="text" name="event_type" placeholder="Event type (optional)">
                <select name="sort_by">
                    <option value="name">Sort by Name</option>
                    <option value="date">Sort by Date</option>
                </select>
                <button type="submit">Search</button>
            </form>
            {% if error %}<p>{{ error }}</p>{% endif %}
            {% if events %}
                <h2>Events:</h2>
                <ul>
                {% for event in events %}
                    <li>{{ event.name }} - {{ event.dates.start.localDate|default('TBD') }}</li>
                {% endfor %}
                </ul>
            {% endif %}
        </body>
        </html>
    """, events=events, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
