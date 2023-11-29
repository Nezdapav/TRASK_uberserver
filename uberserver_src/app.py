from fastapi import FastAPI

from datetime import datetime
from uberserver_src.gps_server.gps_server_client import GPSServerClient
from fastapi import Depends

from uberserver_src.models.models import CurrentTimeResponse, CurrentPositionResponse

app = FastAPI()


@app.get("/v1/now", response_model=CurrentTimeResponse)
def current_time():
    now = datetime.now()
    return CurrentTimeResponse(now=now)


@app.get("/v1/VIP/{point_in_time}", response_model=CurrentPositionResponse)
def position(point_in_time: int, gps_server_client: GPSServerClient = Depends()):
    return gps_server_client.vip_position(point_in_time)