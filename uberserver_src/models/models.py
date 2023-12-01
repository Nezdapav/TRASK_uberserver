from datetime import datetime

from humps import camel
from pydantic import BaseModel, Field


def to_camel(string: str) -> str:
    return camel.case(string)


class CamelBaseModel(BaseModel):
    class Config:
        populate_by_name = True
        alias_generator = to_camel


class VIPGPSCoordsResponse(BaseModel):
    lat: float = Field(alias="latitude")
    long: float = Field(alias="longitude")


class GPSCoords(BaseModel):
    lat: float
    long: float


class CurrentPositionResponse(CamelBaseModel):
    source: str
    gps_coords: GPSCoords = Field("gpsCoords")


class CurrentTimeResponse(BaseModel):
    now: datetime
