from pydantic import BaseModel

class Vehicle(BaseModel):
    route_id: str
    latitude: float
    longitude: float
    timestamp: int

    def to_dict(self):
        return {
            "route_id": self.route_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timestamp": self.timestamp,
        }
