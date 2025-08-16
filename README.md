# Flask Weather App

Current + 5-day forecast using OpenWeatherMap, SQLite CRUD, and optional Google Maps embed.

## Features
- Current weather + 5-day (3-hour) forecast via OpenWeatherMap
- SQLite with CRUD (Create, Read, Update, Delete)
- Optional Google Maps embed (works without the key)
- Modular: runs even if GOOGLE_MAPS_API_KEY is missing

## Project Structure
```
weather_app/
├── app.py
├── models.py
├── templates/
│   ├── layout.html
│   ├── index.html
│   ├── results.html
│   ├── edit.html
│   └── records.html
├── static/
│   ├── style.css
│   └── script.js
├── requirements.txt
├── .env.example
└── README.md
```

## Setup
1. Python 3.10+
2. Create virtual env and install:
```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```
3. Create `.env` from example and fill values:
```
OPENWEATHER_API_KEY=your_openweather_api_key
GOOGLE_MAPS_API_KEY=optional
FLASK_SECRET_KEY=change_me
```
4. Run the app:
```bash
python app.py
```
Open http://127.0.0.1:5000

## Notes
- If `OPENWEATHER_API_KEY` is missing, form submissions will error with a helpful message.
- If `GOOGLE_MAPS_API_KEY` is missing, the map section is hidden.
- Data is stored in `weather.db` (SQLite) in the project root.
