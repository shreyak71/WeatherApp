from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance to be initialized by the Flask app

db = SQLAlchemy()


class WeatherRecord(db.Model):
    __tablename__ = "weather_records"

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    date_range = db.Column(db.String(50), nullable=False)
    weather_data = db.Column(db.Text, nullable=False)  # store as JSON string
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    __table_args__ = (db.UniqueConstraint('location', 'date_range', name='_location_date_uc'),)

    def __repr__(self) -> str:
        return f"<WeatherRecord {self.location}>"
