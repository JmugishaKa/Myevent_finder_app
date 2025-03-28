# Local Event Finder
CLI locally, web app deployed.

# Description
This is an app that tracks down social events from different places, which for now we can track on ticketmaster and eventbrite, targeting users who like grand events.

## Local Setup (CLI)
1. Clone: `git clone url`
2. Install: `pip3 install requests python-dotenv`
3. Add `.env` with `TICKETMASTER_API_KEY and EVENBRITE_API_KEY`
4. Run: `python3 event_finder.py`

## Deployment (Web)
- Web01/Web02: Clone, install Python/Flask, run `gunicorn --bind 0.0.0.0:5000 app:app`.
- Lb01: Install Nginx, configure upstream, restart.
- Access: `http://lb01_ip`
# Example of Places (depending on what the api can find).
1. New York,
2. 
## API
- Ticketmaster Discovery API v2: https://developer.ticketmaster.com/
- eventbrite API: https://developer.eventbrite.com
- Credit: Ticketmaster Team and eventbrite team.
