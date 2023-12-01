import logging
import time
from datetime import datetime

import pytz
from fastapi import Depends, FastAPI, Path, Request
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_fastapi_instrumentator.routing import get_route_name

from uberserver_src.authentication_server.authentication_server import \
    require_authentication
from uberserver_src.errors.authentication_errors import (AuthenticationError,
                                                         BadCredentials,
                                                         ForbiddenUser)
from uberserver_src.errors.gps_server_client_errors import UberServerError
from uberserver_src.gps_server.gps_server_client import GPSServerClient
from uberserver_src.metrics import (increment_errors_total,
                                    request_duration_seconds)
from uberserver_src.models.models import (CurrentPositionResponse,
                                          CurrentTimeResponse, GPSCoords)

logging.basicConfig(filename="./logs.txt", level=logging.DEBUG)
logger = logging.getLogger("uberServer")

prometheus_instrumentator = Instrumentator(
    should_group_status_codes=True,
)

prometheus_instrumentator.add(request_duration_seconds())

app = FastAPI()

prometheus_instrumentator.instrument(app)
prometheus_instrumentator.expose(app, include_in_schema=True)


@app.exception_handler(AuthenticationError)
def authentication_error(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, BadCredentials):
        return JSONResponse(
            status_code=401,
            content={"error_message": "Bad credentials."},
        )
    if isinstance(exc, ForbiddenUser):
        return JSONResponse(
            status_code=403,
            content={"error_message": "Forbidden user."},
        )
    return JSONResponse(
        status_code=500,
        content={"error_message": "Internal server error."},
    )


@app.exception_handler(UberServerError)
def gps_server_error(request: Request, exc: Exception) -> JSONResponse:
    logger.warning(type(exc))
    return JSONResponse(
        status_code=500,
        content={"error_message": "Internal server error"},
    )


@app.exception_handler(Exception)
def general_exception(request: Request, exc: Exception) -> JSONResponse:
    increment_errors_total(exception_name=str(type(exc)), endpoint=get_route_name(request) or "")
    logger.exception(exc)
    return JSONResponse(
        status_code=500,
        content={"error_message": "Internal server error"},
    )


@app.get("/v1/now", response_model=CurrentTimeResponse)
def current_time():
    now = datetime.now(pytz.utc).replace(microsecond=0)
    return CurrentTimeResponse(now=now)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    logger.info(f"completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response


@app.get("/v1/VIP/{point_in_time}", response_model=CurrentPositionResponse)
def position(
    point_in_time: int = Path(),
    gps_server_client: GPSServerClient = Depends(),
    auth=Depends(require_authentication()),
):
    gps_coords = gps_server_client.vip_position(point_in_time)
    return CurrentPositionResponse(
        source="vip-db", gps_coords=GPSCoords.parse_obj(gps_coords.dict())
    )
