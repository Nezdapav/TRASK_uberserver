from pydantic import BaseModel
from datetime import datetime


class GPSCoords(BaseModel):
    lat: float
    long: float


class CurrentPositionResponse(BaseModel):
    source: str
    gps_coords: GPSCoords


class CurrentTimeResponse(BaseModel):
    now: datetime
