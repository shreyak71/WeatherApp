import os
import json
import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

from models import db, WeatherRecord

# Load environment variables
load_dotenv()


def create_app() -> Flask:
    app = Flask(__name__)

    # Secret key
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

    # Configure DB
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weather.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize DB
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # API Keys
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")

    # Helper to fetch weather
    def get_weather(location: str):
        if not OPENWEATHER_API_KEY:
            return {"cod": 401, "message": "Missing OPENWEATHER_API_KEY"}, {}
        base = "https://api.openweathermap.org/data/2.5"
        current_url = f"{base}/weather?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"
        forecast_url = f"{base}/forecast?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"
        try:
            weather_resp = requests.get(current_url, timeout=15)
            forecast_resp = requests.get(forecast_url, timeout=15)
            weather_json = weather_resp.json()
            forecast_json = forecast_resp.json()
            return weather_json, forecast_json
        except requests.RequestException as e:
            return {"cod": 500, "message": str(e)}, {}

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            location = request.form.get("location", "").strip()
            date_range = request.form.get("date_range", "").strip()

            if not location or not date_range:
                flash("Please enter both location and date range", "error")
                return redirect(url_for("index"))

            weather_resp, forecast_resp = get_weather(location)

            try:
                cod = int(weather_resp.get("cod", 0))
            except Exception:
                cod = 0
            if cod != 200:
                msg = weather_resp.get("message", "Invalid location or API error")
                flash(f"Error: {msg}", "error")
                return redirect(url_for("index"))

            # Check for existing record
            record = WeatherRecord.query.filter_by(location=location, date_range=date_range).first()

            if record:
                # Update existing record's weather data
                record.weather_data = json.dumps({"current": weather_resp, "forecast": forecast_resp})
            else:
                # Create new record
                record = WeatherRecord(
                    location=location,
                    date_range=date_range,
                    weather_data=json.dumps({"current": weather_resp, "forecast": forecast_resp}),
                )
                db.session.add(record)

            db.session.commit()

            return redirect(url_for("results", record_id=record.id))
        return render_template("index.html")

    @app.route("/results/<int:record_id>")
    def results(record_id: int):
        record = WeatherRecord.query.get_or_404(record_id)
        data = json.loads(record.weather_data)
        return render_template("results.html", record=record, data=data, maps_key=GOOGLE_MAPS_API_KEY)

    @app.route("/records")
    def records():
        all_records = WeatherRecord.query.order_by(WeatherRecord.id.desc()).all()
        return render_template("records.html", records=all_records)

    @app.route("/edit/<int:record_id>", methods=["GET", "POST"])
    def edit(record_id: int):
        record = WeatherRecord.query.get_or_404(record_id)
        if request.method == "POST":
            record.location = request.form.get("location", record.location).strip()
            record.date_range = request.form.get("date_range", record.date_range).strip()
            weather_resp, forecast_resp = get_weather(record.location)
            try:
                cod = int(weather_resp.get("cod", 0))
            except Exception:
                cod = 0
            if cod == 200:
                record.weather_data = json.dumps({"current": weather_resp, "forecast": forecast_resp})
            else:
                flash("Could not refresh weather for updated location.", "warning")
            db.session.commit()
            return redirect(url_for("records"))
        return render_template("edit.html", record=record)

    @app.route("/delete/<int:record_id>", methods=["POST"]) 
    def delete(record_id: int):
        record = WeatherRecord.query.get_or_404(record_id)
        db.session.delete(record)
        db.session.commit()
        flash("Record deleted", "success")
        return redirect(url_for("records"))

    return app


# Create app instance for Gunicorn
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
