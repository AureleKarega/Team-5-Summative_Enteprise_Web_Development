import pandas as pd
import numpy as np
from datetime import datetime
from logging import getLogger

logger = getLogger(__name__)

# Safety small value to avoid division by zero
EPSILON = 1e-6


def basic_clean(df: pd.DataFrame):
    """
    Apply basic cleaning rules and return cleaned df and a logged DataFrame of removed rows.
    Rules:
      - drop rows with missing pickup or dropoff time
      - drop rows with missing trip_duration or non-positive duration
      - drop rows with negative fare (if present)
      - compute parsed datetimes
      - calculate trip_distance from coordinates
    """
    removed = []

    # Standardize column names (attempt common variants)
    rename_map = {}
    if 'tpep_pickup_datetime' in df.columns:
        rename_map['tpep_pickup_datetime'] = 'pickup_datetime'
    if 'tpep_dropoff_datetime' in df.columns:
        rename_map['tpep_dropoff_datetime'] = 'dropoff_datetime'

    # apply rename if any
    if rename_map:
        df = df.rename(columns=rename_map)

    # Parse datetimes
    for col in ['pickup_datetime', 'dropoff_datetime']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # missing essential fields (pickup/dropoff times and duration)
    mask_missing = df['pickup_datetime'].isna() | df['dropoff_datetime'].isna()
    if 'trip_duration' in df.columns:
        mask_missing = mask_missing | df['trip_duration'].isna()

    if mask_missing.any():
        removed.append(("missing_essential", df[mask_missing]))
        df = df[~mask_missing]

    # trip_duration must be > 0
    if 'trip_duration' in df.columns:
        mask_nonpos_duration = df['trip_duration'] <= 0
        if mask_nonpos_duration.any():
            removed.append(("non_positive_duration", df[mask_nonpos_duration]))
            df = df[~mask_nonpos_duration]
    else:
        # Calculate trip_duration from datetime columns
        df['trip_duration'] = (df['dropoff_datetime'] - df['pickup_datetime']).dt.total_seconds()
        mask_nonpos_duration = df['trip_duration'] <= 0
        if mask_nonpos_duration.any():
            removed.append(("non_positive_duration", df[mask_nonpos_duration]))
            df = df[~mask_nonpos_duration]

    # Calculate trip_distance from coordinates using Haversine formula
    df['trip_distance'] = calculate_distance(
        df['pickup_latitude'],
        df['pickup_longitude'],
        df['dropoff_latitude'],
        df['dropoff_longitude']
    )

    # Drop rows with invalid coordinates (resulting in NaN distance)
    mask_invalid_distance = df['trip_distance'].isna()
    if mask_invalid_distance.any():
        removed.append(("invalid_coordinates", df[mask_invalid_distance]))
        df = df[~mask_invalid_distance]

    # trip_distance must be > 0
    mask_nonpos_dist = df['trip_distance'] <= 0
    if mask_nonpos_dist.any():
        removed.append(("non_positive_distance", df[mask_nonpos_dist]))
        df = df[~mask_nonpos_dist]

    # negative fares (if fare column exists)
    if 'fare_amount' in df.columns:
        mask_neg_fare = df['fare_amount'] < 0
        if mask_neg_fare.any():
            removed.append(("negative_fare", df[mask_neg_fare]))
            df = df[~mask_neg_fare]

    # cap outliers: drop trips with distance > 300 km or duration > 48 hours (tuneable)
    mask_dist_outlier = df['trip_distance'] > 300
    if mask_dist_outlier.any():
        removed.append(("distance_outlier", df[mask_dist_outlier]))
        df = df[~mask_dist_outlier]

    mask_duration_outlier = df['trip_duration'] > 48 * 3600
    if mask_duration_outlier.any():
        removed.append(("duration_outlier", df[mask_duration_outlier]))
        df = df[~mask_duration_outlier]

    # Reset index
    df = df.reset_index(drop=True)

    # combine removed reason frames into one for logging
    removed_df = pd.concat([r[1] for r in removed]) if removed else pd.DataFrame()
    # return cleaned df and removed_df with reasons
    reasons = []
    for reason, frame in removed:
        reasons.append((reason, frame.shape[0]))
        logger.info(f"Removed {frame.shape[0]} rows for reason: {reason}")

    return df, removed_df, reasons


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two coordinates using Haversine formula.
    Returns distance in kilometers.

    Args:
        lat1, lon1: Starting coordinates
        lat2, lon2: Ending coordinates

    Returns:
        Distance in kilometers
    """
    # Radius of Earth in kilometers
    R = 6371.0

    # Convert to radians
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)

    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = np.sin(dlat / 2) ** 2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    distance = R * c

    return distance


def advanced_clean_and_enrich(df: pd.DataFrame):
    """
    Derived feature engineering: trip_duration already present.
    Compute average_speed_kmph, fare_per_km, pickup_hour, day_of_week
    """
    # trip_distance is already in km from calculate_distance
    df['trip_distance_km'] = df['trip_distance']

    # ensure trip_duration in seconds present
    if 'trip_duration' not in df.columns:
        df['trip_duration'] = (
                    pd.to_datetime(df['dropoff_datetime']) - pd.to_datetime(df['pickup_datetime'])).dt.total_seconds()

    # trip_duration_hours
    df['trip_duration_hours'] = df['trip_duration'] / 3600.0 + EPSILON

    # average speed km/h
    df['average_speed_kmph'] = df['trip_distance_km'] / df['trip_duration_hours']
    # handle infs or very large speeds: cap
    df.loc[df['average_speed_kmph'] > 300, 'average_speed_kmph'] = np.nan

    # fare per km (if fare_amount exists)
    if 'fare_amount' in df.columns:
        df['fare_per_km'] = df['fare_amount'] / (df['trip_distance_km'] + EPSILON)
    else:
        df['fare_per_km'] = np.nan

    df['pickup_hour'] = pd.to_datetime(df['pickup_datetime']).dt.hour
    df['day_of_week'] = pd.to_datetime(df['pickup_datetime']).dt.dayofweek

    # drop temp helper column trip_duration_hours
    df = df.drop(columns=['trip_duration_hours'])

    return df
