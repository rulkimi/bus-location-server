from pydantic import BaseModel

class Vehicle(BaseModel):
    route_id: str
    latitude: float
    longitude: float
    timestamp: int