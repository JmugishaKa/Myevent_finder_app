# Local Event Finder
CLI locally, web app deployed.

## Local Setup (CLI)
1. Clone: `git clone url`
2. Install: `pip3 install requests python-dotenv`
3. Add `.env` with `TICKETMASTER_API_KEY`
4. Run: `python3 event_finder.py`

## Deployment (Web)
- Web01/Web02: Clone, install Python/Flask, run `gunicorn --bind 0.0.0.0:5000 app:app`.
- Lb01: Install Nginx, configure upstream, restart.
- Access: `http://lb01_ip`

## API
- Ticketmaster Discovery API v2: https://developer.ticketmaster.com/
- Credit: Ticketmaster Team
