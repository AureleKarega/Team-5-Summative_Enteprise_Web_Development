#!/usr/bin/env python3
import csv
import os
import sys
from datetime import datetime
import logging

# Add the parent directory (project root) to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Now use absolute imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import Config
from src.models.trip import Trip
from src.extensions import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def row_to_trip_dict(row):
    """
    Map CSV row keys to Trip model fields. Assumes processed CSV has these columns.
    """

    def safe_float(x):
        try:
            return float(x) if x != '' else None
        except:
            return None

    def safe_int(x):
        try:
            return int(float(x)) if x != '' else None
        except:
            return None

    def safe_dt(x):
        try:
            return datetime.fromisoformat(x)
        except:
            return None

    return {
        "vendor_id": safe_int(row.get("vendor_id", "")),
        "pickup_datetime": safe_dt(row.get("pickup_datetime", "")),
        "dropoff_datetime": safe_dt(row.get("dropoff_datetime", "")),
        "passenger_count": safe_int(row.get("passenger_count", "")),
        "trip_distance": safe_float(row.get("trip_distance", "")),
        "pickup_longitude": safe_float(row.get("pickup_longitude", "")),
        "pickup_latitude": safe_float(row.get("pickup_latitude", "")),
        "dropoff_longitude": safe_float(row.get("dropoff_longitude", "")),
        "dropoff_latitude": safe_float(row.get("dropoff_latitude", "")),
        "fare_amount": safe_float(row.get("fare_amount", "")),
        "tip_amount": safe_float(row.get("tip_amount", "")),
        "payment_type": row.get("payment_type", None),
        "trip_duration": safe_float(row.get("trip_duration", "")),
        "average_speed_kmph": safe_float(row.get("average_speed_kmph", "")),
        "fare_per_km": safe_float(row.get("fare_per_km", "")),
        "pickup_hour": safe_int(row.get("pickup_hour", "")),
        "day_of_week": safe_int(row.get("day_of_week", "")),
    }


def bulk_insert(session, rows):
    """
    session: SQLAlchemy session
    rows: list of dicts mapping Trip fields
    Use SQLAlchemy bulk_insert_mappings for speed.
    """
    try:
        session.bulk_insert_mappings(Trip, rows)
        session.commit()
        logger.info(f"Successfully inserted {len(rows)} rows")
    except Exception as e:
        session.rollback()
        logger.error(f"Error inserting batch: {e}")
        raise


def main(csv_path, batch_size=5000, db_url=None):
    if db_url is None:
        db_url = Config.SQLALCHEMY_DATABASE_URI

    logger.info(f"Connecting to database: {db_url}")
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    total = 0
    batch = []

    logger.info(f"Reading CSV from: {csv_path}")

    try:
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                trip = row_to_trip_dict(row)
                batch.append(trip)
                if len(batch) >= batch_size:
                    bulk_insert(session, batch)
                    total += len(batch)
                    logger.info(f"Inserted {total} rows so far...")
                    batch = []

            # Insert remaining rows
            if batch:
                bulk_insert(session, batch)
                total += len(batch)
                logger.info(f"Inserted final batch. Total: {total} rows")

        logger.info("Import complete.")
    except Exception as e:
        logger.error(f"Error during import: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "data/processed/trips_cleaned.csv"
    main(csv_path)