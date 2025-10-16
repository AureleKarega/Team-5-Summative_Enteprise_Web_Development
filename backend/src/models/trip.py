from ..extensions import db
from sqlalchemy import Index

class Trip(db.Model):
    __tablename__ = "trips"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    vendor_id = db.Column(db.Integer, nullable=True)
    pickup_datetime = db.Column(db.DateTime, nullable=False, index=True)
    dropoff_datetime = db.Column(db.DateTime, nullable=False)
    passenger_count = db.Column(db.Integer, nullable=True)
    trip_distance = db.Column(db.Float, nullable=False, index=True)
    pickup_longitude = db.Column(db.Float, nullable=True)
    pickup_latitude = db.Column(db.Float, nullable=True)
    dropoff_longitude = db.Column(db.Float, nullable=True)
    dropoff_latitude = db.Column(db.Float, nullable=True)
    fare_amount = db.Column(db.Float, nullable=True)
    tip_amount = db.Column(db.Float, nullable=True)
    payment_type = db.Column(db.String(32), nullable=True)

    # Derived features
    trip_duration = db.Column(db.Float, nullable=True)      # seconds
    average_speed_kmph = db.Column(db.Float, nullable=True)
    fare_per_km = db.Column(db.Float, nullable=True)
    pickup_hour = db.Column(db.Integer, nullable=True)
    day_of_week = db.Column(db.Integer, nullable=True)  # 0=Monday

    __table_args__ = (
        Index('ix_trips_pickup_dt_distance', "pickup_datetime", "trip_distance"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "vendor_id": self.vendor_id,
            "pickup_datetime": self.pickup_datetime.isoformat() if self.pickup_datetime else None,
            "dropoff_datetime": self.dropoff_datetime.isoformat() if self.dropoff_datetime else None,
            "passenger_count": self.passenger_count,
            "trip_distance": self.trip_distance,
            "pickup_longitude": self.pickup_longitude,
            "pickup_latitude": self.pickup_latitude,
            "dropoff_longitude": self.dropoff_longitude,
            "dropoff_latitude": self.dropoff_latitude,
            "fare_amount": self.fare_amount,
            "tip_amount": self.tip_amount,
            "trip_duration": self.trip_duration,
            "average_speed_kmph": self.average_speed_kmph,
            "fare_per_km": self.fare_per_km,
            "pickup_hour": self.pickup_hour,
            "day_of_week": self.day_of_week,
        }
