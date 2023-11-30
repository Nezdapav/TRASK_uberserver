from humps import camel
from pydantic import BaseModel, Field
from datetime import datetime


def to_camel(string: str) -> str:
    return camel.case(string)


class CamelBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
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
