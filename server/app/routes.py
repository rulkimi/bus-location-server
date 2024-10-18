from fastapi import APIRouter, HTTPException
from app.utils import fetch_gtfs_realtime_feed, process_feed, extract_vehicle_data, reverse_geocode

router = APIRouter()

# Sample GTFS-R URLs
FEEDER_BUS_URL = 'https://api.data.gov.my/gtfs-realtime/vehicle-position/prasarana?category=rapid-bus-mrtfeeder'
RAPID_KL_URL = 'https://api.data.gov.my/gtfs-realtime/vehicle-position/prasarana?category=rapid-bus-kl'

@router.get("/")
def read_root():
    return {"message": "Welcome to the Bus Location API"}


@router.get("/routes")
def get_routes():
    print("Fetching feeder bus and Rapid KL bus feeds")
    
    # Fetch feeds for feeder buses and Rapid KL buses
    feeder_bus_content = fetch_gtfs_realtime_feed(FEEDER_BUS_URL)
    rapid_kl_content = fetch_gtfs_realtime_feed(RAPID_KL_URL)

    # Check if feeds were fetched successfully
    if not feeder_bus_content and not rapid_kl_content:
        print("Failed to fetch both feeder bus and Rapid KL feeds.")
        raise HTTPException(status_code=500, detail="Failed to fetch bus data.")

    # Initialize separate lists for feeder buses and Rapid KL buses
    feeder_routes = []
    rapid_kl_routes = []

    # Process feeder buses
    if feeder_bus_content:
        print("Processing feeder bus feed")
        feeder_vehicles = process_feed(feeder_bus_content)
        for vehicle in feeder_vehicles:
            vehicle_data = extract_vehicle_data(vehicle)
            if vehicle_data.latitude and vehicle_data.longitude:
                feeder_routes.append({
                    "route_id": vehicle_data.route_id,
                    "latitude": vehicle_data.latitude,
                    "longitude": vehicle_data.longitude,
                    "timestamp": vehicle_data.timestamp,
                })

    # Process Rapid KL buses
    if rapid_kl_content:
        print("Processing Rapid KL bus feed")
        rapid_kl_vehicles = process_feed(rapid_kl_content)
        for vehicle in rapid_kl_vehicles:
            vehicle_data = extract_vehicle_data(vehicle)
            if vehicle_data.latitude and vehicle_data.longitude:
                rapid_kl_routes.append({
                    "route_id": vehicle_data.route_id,
                    "latitude": vehicle_data.latitude,
                    "longitude": vehicle_data.longitude,
                    "timestamp": vehicle_data.timestamp,
                })

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

    # Apply sorting
    feeder_routes = sorted(feeder_routes, key=sort_key)
    rapid_kl_routes = sorted(rapid_kl_routes, key=sort_key)

    # Remove duplicates by route_id
    def remove_duplicates(routes):
        seen_route_ids = set()
        unique_routes = []
        for route in routes:
            if route["route_id"] not in seen_route_ids:
                unique_routes.append(route)
                seen_route_ids.add(route["route_id"])
        return unique_routes

    # Filter out duplicate routes
    feeder_routes = remove_duplicates(feeder_routes)
    rapid_kl_routes = remove_duplicates(rapid_kl_routes)

    print(f"Found {len(feeder_routes)} unique feeder routes and {len(rapid_kl_routes)} unique Rapid KL routes.")
    
    # Return both lists separately, sorted and with duplicates removed
    return {
        "feeder_bus_active_routes": feeder_routes,
        "rapid_kl_active_routes": rapid_kl_routes
    }

@router.get("/vehicle/{route_id}")
def get_vehicle_by_route(route_id: str):
    print(f"Searching for vehicles on route: {route_id}")
    
    # Fetch feeds from both sources
    feeder_bus_content = fetch_gtfs_realtime_feed(FEEDER_BUS_URL)
    rapid_kl_content = fetch_gtfs_realtime_feed(RAPID_KL_URL)

    if not feeder_bus_content and not rapid_kl_content:
        print("Failed to fetch any bus feeds.")
        raise HTTPException(status_code=500, detail="Failed to fetch bus data.")

    vehicles = []

    # Process feeder bus feed
    if feeder_bus_content:
        print("Processing feeder bus vehicles")
        feeder_feed = gtfs_realtime_pb2.FeedMessage()
        feeder_feed.ParseFromString(feeder_bus_content)
        vehicles.extend([MessageToDict(entity.vehicle) for entity in feeder_feed.entity])

    # Process rapid KL feed
    if rapid_kl_content:
        print("Processing Rapid KL vehicles")
        rapid_kl_feed = gtfs_realtime_pb2.FeedMessage()
        rapid_kl_feed.ParseFromString(rapid_kl_content)
        vehicles.extend([MessageToDict(entity.vehicle) for entity in rapid_kl_feed.entity])

    # Extract relevant vehicle data
    vehicles_on_route = []
    for vehicle in vehicles:
        vehicle_route_id = vehicle.get('trip', {}).get('routeId', 'N/A')
        if vehicle_route_id.lower() == route_id.lower():
            print(f"Raw vehicle data: {vehicle}")

            vehicle_id = vehicle.get('vehicle', {}).get('id', 'N/A')
            latitude = vehicle.get('position', {}).get('latitude')
            longitude = vehicle.get('position', {}).get('longitude')
            timestamp = vehicle.get('timestamp', 'N/A')

            if latitude and longitude:
                location_name = reverse_geocode(latitude, longitude)
                vehicles_on_route.append({
                    "vehicle_id": vehicle_id,
                    "route_id": vehicle_route_id,
                    "latitude": latitude,
                    "longitude": longitude,
                    "timestamp": int(timestamp),
                    "location": location_name or "Unknown location"
                })

    if not vehicles_on_route:
        print(f"No vehicles found on route: {route_id}")
        raise HTTPException(status_code=404, detail="No bus found for the specified route.")

    print(f"Found {len(vehicles_on_route)} vehicles on route: {route_id}")
    return {"vehicles": vehicles_on_route}
