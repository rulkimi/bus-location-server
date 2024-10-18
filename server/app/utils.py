import time
from requests import get
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
from requests.exceptions import RequestException
from app.models import Vehicle

def fetch_gtfs_realtime_feed(url):
    retries = 5
    for attempt in range(retries):
        try:
            print(f"Fetching GTFS feed from {url}, attempt {attempt + 1}")
            response = get(url)
            response.raise_for_status()
            print(f"Successfully fetched GTFS feed from {url}")
            return response.content
        except RequestException as e:
            print(f"Error fetching GTFS Realtime feed: {e}")
            time.sleep(5)
    print(f"Failed to fetch GTFS feed after {retries} attempts.")
    return None

def reverse_geocode(lat, lon):
    try:
        print(f"Reverse geocoding coordinates: lat={lat}, lon={lon}")
        geolocator = Nominatim(user_agent='azruldauntless@gmail.com')
        location = geolocator.reverse((lat, lon), exactly_one=True)
        if location:
            print(f"Reverse geocoded location: {location.address}")
        return location.address if location else None
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Error in reverse geocoding: {e}")
        return None

def process_feed(content):
    print("Processing GTFS feed content")
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(content)
    vehicles = [MessageToDict(entity.vehicle) for entity in feed.entity]
    print(f"Processed {len(vehicles)} vehicles from feed")
    return vehicles

def extract_vehicle_data(vehicle):
    route_id = vehicle.get('trip', {}).get('routeId', 'N/A')
    latitude = vehicle.get('position', {}).get('latitude')
    longitude = vehicle.get('position', {}).get('longitude')
    timestamp = vehicle.get('timestamp', 'N/A')
    print(f"Extracted vehicle data: route_id={route_id}, lat={latitude}, lon={longitude}, timestamp={timestamp}")
    return Vehicle(route_id=route_id, latitude=latitude, longitude=longitude, timestamp=timestamp)

# Sort the routes by alphabet and by number (custom sorting)
def sort_key(route):
    # Separate alphabetic and numeric parts of the route_id for proper sorting
    import re
    match = re.match(r"([a-zA-Z]+)(\d+)?", route["route_id"])
    if match:
        alpha_part = match.group(1)
        numeric_part = int(match.group(2)) if match.group(2) else 0
        return (alpha_part, numeric_part)
    return (route["route_id"], 0)  # Default in case no match

# Remove duplicates by route_id
def remove_duplicates(routes):
    seen_route_ids = set()
    unique_routes = []
    for route in routes:
        if route["route_id"] not in seen_route_ids:
            unique_routes.append(route)
            seen_route_ids.add(route["route_id"])
    return unique_routes

def process_bus_feed(content):
    """Process the GTFS feed content and extract vehicle data."""
    if not content:
        return []
    
    vehicles = process_feed(content)
    routes = []
    for vehicle in vehicles:
        vehicle_data = extract_vehicle_data(vehicle)
        if vehicle_data.latitude and vehicle_data.longitude:
            routes.append({
                "route_id": vehicle_data.route_id,
                "latitude": vehicle_data.latitude,
                "longitude": vehicle_data.longitude,
                "timestamp": vehicle_data.timestamp,
            })
    return routes