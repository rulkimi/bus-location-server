from fastapi import APIRouter, HTTPException
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
from app.utils import fetch_gtfs_realtime_feed, reverse_geocode, sort_key, remove_duplicates, process_bus_feed

router = APIRouter()

# GTFS-R URLs
FEEDER_BUS_URL = 'https://api.data.gov.my/gtfs-realtime/vehicle-position/prasarana?category=rapid-bus-mrtfeeder'
RAPID_KL_URL = 'https://api.data.gov.my/gtfs-realtime/vehicle-position/prasarana?category=rapid-bus-kl'

@router.get("/routes")
def get_routes():

    print("Fetching feeder bus and Rapid KL bus feeds")
    
    feeder_bus_content = fetch_gtfs_realtime_feed(FEEDER_BUS_URL)
    rapid_kl_content = fetch_gtfs_realtime_feed(RAPID_KL_URL)

    if not feeder_bus_content and not rapid_kl_content:
        print("Failed to fetch both feeder bus and Rapid KL feeds.")
        raise HTTPException(status_code=500, detail="Failed to fetch bus data.")

    feeder_routes = remove_duplicates(sorted(process_bus_feed(feeder_bus_content), key=sort_key))
    rapid_kl_routes = remove_duplicates(sorted(process_bus_feed(rapid_kl_content), key=sort_key))

    print(f"Found {len(feeder_routes)} unique feeder routes and {len(rapid_kl_routes)} unique Rapid KL routes.")
    
    return {
        "feeder_bus_active_routes": feeder_routes,
        "rapid_kl_active_routes": rapid_kl_routes
    }

@router.get("/vehicle/{route_id}")
def get_vehicle_by_route(route_id: str):

    print(f"Searching for vehicles on route: {route_id}")
    
    feeder_bus_content = fetch_gtfs_realtime_feed(FEEDER_BUS_URL)
    rapid_kl_content = fetch_gtfs_realtime_feed(RAPID_KL_URL)

    if not feeder_bus_content and not rapid_kl_content:
        raise HTTPException(status_code=500, detail="Failed to fetch bus data.")

    vehicles = []

    if feeder_bus_content:
        feeder_feed = gtfs_realtime_pb2.FeedMessage()
        feeder_feed.ParseFromString(feeder_bus_content)
        vehicles.extend([MessageToDict(entity.vehicle) for entity in feeder_feed.entity])

    if rapid_kl_content:
        rapid_kl_feed = gtfs_realtime_pb2.FeedMessage()
        rapid_kl_feed.ParseFromString(rapid_kl_content)
        vehicles.extend([MessageToDict(entity.vehicle) for entity in rapid_kl_feed.entity])

    vehicles_on_route = []
    for vehicle in vehicles:
        vehicle_route_id = vehicle.get('trip', {}).get('routeId', 'N/A')
        if vehicle_route_id.lower() == route_id.lower():
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
        raise HTTPException(status_code=404, detail="No bus found for the specified route.")

    print(f"Found {len(vehicles_on_route)} vehicles on route: {route_id}")
    return {"vehicles": vehicles_on_route}
