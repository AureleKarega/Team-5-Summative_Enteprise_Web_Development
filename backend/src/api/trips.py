from flask import Blueprint, request, jsonify
from sqlalchemy import func
from src.models.trip import Trip
from src.services_custom.top_k_hotspots import top_k_hotspots

trips_bp = Blueprint('trips', __name__)

@trips_bp.route('', methods=['GET'])
def list_trips():
    """
    Simple listing endpoint with filters:
    - start, end: ISO datetimes for pickup
    - min_distance, max_distance
    - limit: number
    """
    start = request.args.get('start')   # ISO datetime string
    end = request.args.get('end')
    min_distance = request.args.get('min_distance', type=float)
    max_distance = request.args.get('max_distance', type=float)
    limit = request.args.get('limit', type=int, default=100)

    q = Trip.query
    if start:
        q = q.filter(Trip.pickup_datetime >= start)
    if end:
        q = q.filter(Trip.pickup_datetime <= end)
    if min_distance is not None:
        q = q.filter(Trip.trip_distance >= min_distance)
    if max_distance is not None:
        q = q.filter(Trip.trip_distance <= max_distance)

    results = q.limit(min(limit, 1000)).all()
    data = [r.to_dict() for r in results]
    return jsonify(data)

@trips_bp.route('/summary', methods=['GET'])
def summary():
    """
    Return simple aggregates over pickups in a time window
    """
    try:
        # Log request details for debugging
        print(f"Summary API called with args: {dict(request.args)}")
        
        start = request.args.get('start')
        end = request.args.get('end')
        
        # Log parsed date values
        print(f"Date range: start={start}, end={end}")
        
        q = Trip.query
        if start:
            q = q.filter(Trip.pickup_datetime >= start)
        if end:
            q = q.filter(Trip.pickup_datetime <= end)

        # Count query - catch and log any DB errors
        try:
            total_trips = q.count()
        except Exception as e:
            print(f"Error in count query: {str(e)}")
            return jsonify({"error": "Database error", "message": str(e)}), 500

        # Average queries
        avg_distance = q.with_entities(func.avg(Trip.trip_distance)).scalar() or 0
        avg_fare = q.with_entities(func.avg(Trip.fare_amount)).scalar() or 0
        avg_speed = q.with_entities(func.avg(Trip.average_speed_kmph)).scalar() or 0

        # Return the data
        response_data = {
            "total_trips": total_trips,
            "avg_distance": float(avg_distance),
            "avg_fare": float(avg_fare),
            "avg_speed_kmph": float(avg_speed)
        }
        print(f"Summary response: {response_data}")
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Unexpected error in summary endpoint: {str(e)}")
        return jsonify({
            "error": "Server error",
            "message": str(e),
            "type": type(e).__name__
        }), 500

@trips_bp.route('/<int:trip_id>', methods=['GET'])
def get_trip(trip_id):
    """
    Get a single trip by ID
    """
    t = Trip.query.get_or_404(trip_id)
    return jsonify(t.to_dict())

@trips_bp.route('/hotspots', methods=['GET'])
def get_hotspots():
    """
    Return the top K pickup hotspots
    """
    start = request.args.get('start')
    end = request.args.get('end')
    k = request.args.get('k', type=int, default=10)
    
    q = Trip.query
    if start:
        q = q.filter(Trip.pickup_datetime >= start)
    if end:
        q = q.filter(Trip.pickup_datetime <= end)
    
    # Limit to avoid memory issues
    trips = q.limit(10000).all()
    trip_dicts = [t.to_dict() for t in trips]
    hotspots = top_k_hotspots(trip_dicts, k=k)
    
    return jsonify(hotspots)

@trips_bp.route('/hourly', methods=['GET'])
def get_hourly_stats():
    """
    Return hourly trip count and average speeds
    """
    start = request.args.get('start')
    end = request.args.get('end')
    
    q = Trip.query
    if start:
        q = q.filter(Trip.pickup_datetime >= start)
    if end:
        q = q.filter(Trip.pickup_datetime <= end)
    
    hours = list(range(24))
    trips_by_hour = []
    speeds_by_hour = []
    
    for hour in hours:
        hour_trips = q.filter(Trip.pickup_hour == hour).count()
        trips_by_hour.append(hour_trips)
        
        avg_speed = q.filter(Trip.pickup_hour == hour).with_entities(
            func.avg(Trip.average_speed_kmph)
        ).scalar() or 0
        speeds_by_hour.append(float(avg_speed))
    
    return jsonify({
        "hours": hours,
        "trips": trips_by_hour,
        "speeds": speeds_by_hour
    })
