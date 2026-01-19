from datetime import datetime, timedelta
from geopy.distance import geodesic
import random
import string

def generate_tracking_number():
    """Generate a unique tracking number"""
    return "TRK" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def calculate_shipping_cost(distance_km: float, weight_kg: float = 1.0):
    """Calculate shipping cost based on distance and weight"""
    base_cost = 50  # Base shipping cost in INR
    distance_cost = distance_km * 2  # 2 INR per km
    weight_cost = weight_kg * 10  # 10 INR per kg
    
    total = base_cost + distance_cost + weight_cost
    return round(total, 2)

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float):
    """Calculate distance between two coordinates in kilometers"""
    return geodesic((lat1, lon1), (lat2, lon2)).kilometers

def estimate_delivery_time(distance_km: float):
    """Estimate delivery time based on distance"""
    # Average speed: 50 km/h
    hours = distance_km / 50
    # Add processing time (1-2 days)
    days = max(1, int(hours / 8) + random.randint(1, 2))
    return datetime.now() + timedelta(days=days)

def update_shipping_location(order_id: str, current_lat: float, current_lon: float, 
                            destination_lat: float, destination_lon: float, status: str):
    """Update shipping location and calculate progress"""
    distance_remaining = calculate_distance(
        current_lat, current_lon, 
        destination_lat, destination_lon
    )
    
    # Simulate shipping progress
    if status == "Shipped":
        # Move 30% towards destination
        progress = 0.3
    elif status == "In Transit":
        # Move 60% towards destination
        progress = 0.6
    elif status == "Out for Delivery":
        # Move 90% towards destination
        progress = 0.9
    else:
        progress = 1.0
    
    # Calculate current position (simplified)
    current_position_lat = current_lat + (destination_lat - current_lat) * progress
    current_position_lon = current_lon + (destination_lon - current_lon) * progress
    
    return {
        "latitude": current_position_lat,
        "longitude": current_position_lon,
        "distance_remaining": round(distance_remaining * (1 - progress), 2),
        "progress_percentage": int(progress * 100)
    }

