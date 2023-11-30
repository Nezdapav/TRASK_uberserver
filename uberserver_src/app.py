import time

import pytz
import logging
from fastapi import FastAPI, Request, Path
from fastapi.responses import JSONResponse

from datetime import datetime

from uberserver_src.authentication_server.authentication_server import require_authentication
from uberserver_src.errors.authentication_errors import AuthenticationError, BadCredentials, \
    ForbiddenUser
from uberserver_src.errors.gps_server_client_errors import UberServerError
from uberserver_src.gps_server.gps_server_client import GPSServerClient
from fastapi import Depends

from uberserver_src.models.models import CurrentTimeResponse, CurrentPositionResponse, GPSCoords
logging.basicConfig(filename="./logs.txt", level=logging.DEBUG)
logger = logging.getLogger("uberServer")
app = FastAPI()


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
    logger.exception(exc)
    return JSONResponse(
        status_code=500,
        content={"error_message": "Internal server error"},
    )


@app.exception_handler(Exception)
def general_exception(request: Request, exc: Exception) -> JSONResponse:
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
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response


@app.get("/v1/VIP/{point_in_time}", response_model=CurrentPositionResponse)
def position(
    point_in_time: int = Path(),
    gps_server_client: GPSServerClient = Depends(),
    auth=Depends(require_authentication()),
):
    gps_coords = gps_server_client.vip_position(point_in_time)
    logger.info(f"Status: 200 URL: /v1/VIP/{point_in_time}")
    return CurrentPositionResponse(source="vip-db", gps_coords=GPSCoords.model_validate(gps_coords))
