import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
from requests import get
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time
from requests.exceptions import RequestException

load_dotenv()

USER_AGENT = os.getenv('EMAIL')

app = FastAPI()

origins = [
    "http://localhost:5173", 
    "http://127.0.0.1:5173",
    "https://rulkimi.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

class Vehicle(BaseModel):
    vehicle_id: str
    route_id: str
    latitude: float
    longitude: float
    timestamp: int

    def to_dict(self):
        return {
            "vehicle_id": self.vehicle_id,
            "route_id": self.route_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timestamp": self.timestamp
        }

# Sample GTFS-R URL from Malaysia's Open API
FEEDER_BUS_URL = 'https://api.data.gov.my/gtfs-realtime/vehicle-position/prasarana?category=rapid-bus-mrtfeeder'
RAPID_KL_URL = 'https://api.data.gov.my/gtfs-realtime/vehicle-position/prasarana?category=rapid-bus-kl'

def fetch_gtfs_realtime_feed(url):
    retries = 5
    for _ in range(retries):
        try:
            response = get(url)
            response.raise_for_status()
            return response.content
        except RequestException as e:
            print(f"Error fetching GTFS Realtime feed: {e}")
            time.sleep(5)  # wait for 5 seconds before retrying
    return None

def reverse_geocode(lat, lon):
    try:
        geolocator = Nominatim(user_agent=USER_AGENT)
        location = geolocator.reverse((lat, lon), exactly_one=True)
        return location.address if location else None
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Error: {e}")
        return None

@app.get("/")
def read_root():
    return {"message": "Welcome to the Bus Location API"}

@app.get("/routes")
def get_routes():
    feeder_bus_content = fetch_gtfs_realtime_feed(FEEDER_BUS_URL)
    rapid_kl_content = fetch_gtfs_realtime_feed(RAPID_KL_URL)

    if not feeder_bus_content or not rapid_kl_content:
        raise HTTPException(status_code=500, detail="Failed to fetch bus data.")

    feeder_feed = gtfs_realtime_pb2.FeedMessage()
    feeder_feed.ParseFromString(feeder_bus_content)
    rapid_kl_feed = gtfs_realtime_pb2.FeedMessage()
    rapid_kl_feed.ParseFromString(rapid_kl_content)

    feeder_vehicles = [MessageToDict(entity.vehicle) for entity in feeder_feed.entity]
    rapid_kl_vehicles = [MessageToDict(entity.vehicle) for entity in rapid_kl_feed.entity]

    feeder_active_routes = set(vehicle.get('trip', {}).get('routeId', 'N/A') for vehicle in feeder_vehicles)
    rapid_kl_active_routes = set(vehicle.get('trip', {}).get('routeId', 'N/A') for vehicle in rapid_kl_vehicles)

    routes = {
        "feeder_bus_active_routes": list(feeder_active_routes),
        "rapid_kl_active_routes": list(rapid_kl_active_routes)
    }

    return routes

@app.get("/vehicle/{route_id}")
def get_vehicle_by_route(route_id: str):
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

    structured_vehicles = []
    for vehicle in vehicles:
        vehicle_id = vehicle.get('vehicle', {}).get('id', 'N/A')
        vehicle_route_id = vehicle.get('trip', {}).get('routeId', 'N/A')
        latitude = vehicle.get('position', {}).get('latitude', 'N/A')
        longitude = vehicle.get('position', {}).get('longitude', 'N/A')
        timestamp = vehicle.get('timestamp', 'N/A')
        structured_vehicle = Vehicle(
            vehicle_id=vehicle_id,
            route_id=vehicle_route_id,
            latitude=latitude,
            longitude=longitude,
            timestamp=timestamp
        )
        structured_vehicles.append(structured_vehicle)

    vehicles_on_route = [vehicle for vehicle in structured_vehicles if vehicle.route_id.lower() == route_id.lower()]

    if not vehicles_on_route:
        raise HTTPException(status_code=404, detail="No bus found for the specified route.")

    result = []
    for vehicle in vehicles_on_route:
        location_name = reverse_geocode(vehicle.latitude, vehicle.longitude)
        result.append({
            "info": vehicle.to_dict(),
            "location": location_name
        })

    return {"vehicles": result}
